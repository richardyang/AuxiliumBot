import discord
import logging
import random
import os

from itertools import chain
from pprint import pformat
import warnings
import torch
import torch.nn.functional as F
from transformers import OpenAIGPTLMHeadModel, OpenAIGPTTokenizer, GPT2LMHeadModel, GPT2Tokenizer
from conv_ai.train import SPECIAL_TOKENS, build_input_from_segments, add_special_tokens_
from conv_ai.utils import get_dataset, download_pretrained_model

from config import conf
from discord.ext import tasks, commands

class Theta(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.src_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))
        
        model_path = os.path.join(self.src_dir, "conv_ai/model/")
        self.args={
            "max_history": 2,
            "device": "cpu",
            "max_length": 20,
            "min_length": 1,
            "temperature": 0.7,
            "top_k": 0,
            "top_p": 0.9,
            "no_sample": 1
        }
        self.tokenizer = OpenAIGPTTokenizer.from_pretrained(model_path)
        self.model = OpenAIGPTLMHeadModel.from_pretrained(model_path)
        self.model.to('cpu')
        add_special_tokens_(self.model, self.tokenizer)
        dataset = get_dataset(self.tokenizer, "", os.path.join(self.src_dir, "conv_ai/dataset_cache"))
        
        self.personalities = [dialog["personality"] for dataset in dataset.values() for dialog in dataset]
        self.personality = random.choice(self.personalities)

        self.history = []
        print("Conversational AI model loaded successfully.")

    @commands.command()
    async def say(self, ctx, *args):
        raw_text = " ".join(args)
        self.history.append(self.tokenizer.encode(raw_text))
        with torch.no_grad():
            out_ids = self.sample_sequence(self.personality, self.history, self.tokenizer, self.model, self.args)
        self.history.append(out_ids)
        self.history = self.history[-(2*self.args["max_history"]+1):]
        out_text = self.tokenizer.decode(out_ids, skip_special_tokens=True)
        
        channel = ctx.message.channel
        await channel.send(out_text)
        return
    
    @commands.command()
    async def aipersonality(self, ctx):
        channel = ctx.message.channel
        await channel.send("AI's current personality: {}".format(self.tokenizer.decode(chain(*self.personality))))
        return

    @commands.command()
    async def changepersonality(self, ctx):
        channel = ctx.message.channel
        self.personality = random.choice(self.personalities)
        await channel.send("AI's new personality: {}".format(self.tokenizer.decode(chain(*self.personality))))
        return

    def top_filtering(self, logits, top_k=0., top_p=0.9, threshold=-float('Inf'), filter_value=-float('Inf')):
        """ Filter a distribution of logits using top-k, top-p (nucleus) and/or threshold filtering
            Args:
                logits: logits distribution shape (vocabulary size)
                top_k: <=0: no filtering, >0: keep only top k tokens with highest probability.
                top_p: <=0.0: no filtering, >0.0: keep only a subset S of candidates, where S is the smallest subset
                    whose total probability mass is greater than or equal to the threshold top_p.
                    In practice, we select the highest probability tokens whose cumulative probability mass exceeds
                    the threshold top_p.
                threshold: a minimal threshold to keep logits
        """
        assert logits.dim() == 1  # Only work for batch size 1 for now - could update but it would obfuscate a bit the code
        top_k = min(top_k, logits.size(-1))
        if top_k > 0:
            # Remove all tokens with a probability less than the last token in the top-k tokens
            indices_to_remove = logits < torch.topk(logits, top_k)[0][..., -1, None]
            logits[indices_to_remove] = filter_value

        if top_p > 0.0:
            # Compute cumulative probabilities of sorted tokens
            sorted_logits, sorted_indices = torch.sort(logits, descending=True)
            cumulative_probabilities = torch.cumsum(F.softmax(sorted_logits, dim=-1), dim=-1)

            # Remove tokens with cumulative probability above the threshold
            sorted_indices_to_remove = cumulative_probabilities > top_p
            # Shift the indices to the right to keep also the first token above the threshold
            sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[..., :-1].clone()
            sorted_indices_to_remove[..., 0] = 0

            # Back to unsorted indices and set them to -infinity
            indices_to_remove = sorted_indices[sorted_indices_to_remove]
            logits[indices_to_remove] = filter_value

        indices_to_remove = logits < threshold
        logits[indices_to_remove] = filter_value

        return logits

    def sample_sequence(self, personality, history, tokenizer, model, args, current_output=None):
        special_tokens_ids = tokenizer.convert_tokens_to_ids(SPECIAL_TOKENS)
        if current_output is None:
            current_output = []

        for i in range(args["max_length"]):
            instance = build_input_from_segments(personality, history, current_output, tokenizer, with_eos=False)

            input_ids = torch.tensor(instance["input_ids"], device=args["device"]).unsqueeze(0)
            token_type_ids = torch.tensor(instance["token_type_ids"], device=args["device"]).unsqueeze(0)

            logits = model(input_ids, token_type_ids=token_type_ids)
            if isinstance(logits, tuple):  # for gpt2 and maybe others
                logits = logits[0]
            logits = logits[0, -1, :] / args["temperature"]
            logits = self.top_filtering(logits, top_k=args["top_k"], top_p=args["top_p"])
            probs = F.softmax(logits, dim=-1)

            prev = torch.topk(probs, 1)[1] if args["no_sample"] else torch.multinomial(probs, 1)
            if i < args["min_length"] and prev.item() in special_tokens_ids:
                while prev.item() in special_tokens_ids:
                    if probs.max().item() == 1:
                        warnings.warn("Warning: model generating special token with probability 1.")
                        break  # avoid infinitely looping over special token
                    prev = torch.multinomial(probs, num_samples=1)

            if prev.item() in special_tokens_ids:
                break
            current_output.append(prev.item())

        return current_output

def setup(bot):
    bot.add_cog(Theta(bot))
    
