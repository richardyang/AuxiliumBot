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
        r = random.randint(0,5)
        if r == 0:
            option = discord.File(os.path.join(self.src_dir,'cogs/gifs/8ball_01.gif'))
        elif r == 1:
            option = discord.File(os.path.join(self.src_dir,'cogs/gifs/8ball_02.gif'))
        elif r == 2:
            option = discord.File(os.path.join(self.src_dir,'cogs/gifs/8ball_03.gif'))
        elif r == 3:
            option = discord.File(os.path.join(self.src_dir,'cogs/gifs/8ball_04.gif'))
        elif r == 4:
            option = discord.File(os.path.join(self.src_dir,'cogs/gifs/8ball_05.gif'))
        else:
            option = discord.File(os.path.join(self.src_dir,'cogs/gifs/8ball_06.gif'))
        msg = await channel.send("The Magic 8 Ball Speaks!", file = option)

def setup(bot):
    bot.add_cog(Fun(bot))