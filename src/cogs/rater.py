import os
import discord

from config import conf
from discord.ext import commands

class LinkRater(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.src_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))

    @commands.Cog.listener()
    async def on_message(self, message):
        # Do nothing if author is self
        if message.author == self.bot.user:
            return
        # Do nothing if author is bot
        if message.author.bot:
            return

        if str(message.channel.id) in conf["RATE_CHANNELS"] and (len(message.embeds) or "http" in message.content):
            await message.add_reaction(emoji="👍")
            await message.add_reaction(emoji="👎")
        else:
            return


def setup(bot):
    bot.add_cog(LinkRater(bot))