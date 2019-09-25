import os
import random
import discord
from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.src_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))

    @commands.command(name='8ball')
    async def eightball(self, ctx):
        channel = ctx.message.channel
        if ctx.message.content.strip() == "-8ball":
            img = discord.File(os.path.join(self.src_dir,'img/8ball_0.png'))
            await channel.send("Type a question after the command!", file=img)
        else:
            r = random.randint(1,5)
            img = discord.File(os.path.join(self.src_dir,'img/8ball_{}.png'.format(r)))
            await channel.send(file=img)
    
    @commands.command()
    async def billy(self, ctx):
        print("Press F for Billy")
        channel = ctx.message.channel
        file = discord.File(os.path.join(self.src_dir, 'img/billy.gif'))
        msg = await channel.send("Press F to pay respects", file=file)
        await msg.add_reaction(emoji="🇫")

def setup(bot):
    bot.add_cog(Fun(bot))