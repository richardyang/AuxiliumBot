import os
import random
import discord
from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.src_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))

    @commands.command(name = '8ball')
    async def eightball(self, ctx):
        channel = ctx.message.channel
        r = random.randint(1,6)
        option = discord.File(os.path.join(self.src_dir,'cogs/gifs/8ball_0{}.gif'.format(r)))
        msg = await channel.send(file = option)

def setup(bot):
    bot.add_cog(Fun(bot))