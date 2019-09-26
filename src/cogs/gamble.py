import os
import random
import discord
from discord.ext import commands

class Gamble(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.src_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))

    @commands.Cog.listener()
    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.bot.user:
            return

        if message.content == 'ping':
            await message.channel.send('pong')

    @commands.command(name = 'flip')
    async def coinflip(self, ctx):
        channel = ctx.message.channel
        r = random.randint(0,100)
        if r < 50:
            coin = discord.File(os.path.join(self.src_dir,'cogs/gifs/coin01.gif'))
        else:
            coin = discord.File(os.path.join(self.src_dir,'cogs/gifs/coin02.gif'))
        msg = await channel.send(file = coin)

    @commands.command(name = 'roll')
    async def rollDie(self, ctx, arg=''):
        if arg == '':
            arg = 1

        arg = int(arg)
        channel = ctx.message.channel
        if arg >= 1 and arg <= 5:
            for x in range(arg):
                r = random.randint(1,6)
                die = discord.File(os.path.join(self.src_dir,'cogs/images/face{}.png' .format(r)))
                msg = await channel.send(file = die)
        elif arg < 1 or arg is None:
            r = random.randint(1,6)
            die = discord.File(os.path.join(self.src_dir,'cogs/images/face{}.png' .format(r)))
            msg = await channel.send(file = die)
        else:
            for x in range(5):
                r = random.randint(1,6)
                die = discord.File(os.path.join(self.src_dir,'cogs/images/face{}.png' .format(r)))
                msg = await channel.send(file = die)

def setup(bot):
    bot.add_cog(Gamble(bot))