import os
import random
import discord

from config import conf
from discord.ext import commands

class Gamble(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.src_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))
        self.economy_cog = self.bot.get_cog("Economy")

    @commands.command(name='coinflip')
    async def coinflip(self, ctx, bet=0):
        bet = abs(bet)
        if bet > 5000:
            await ctx.message.channel.send("Setting your wager amount to the max of 5k.")
            bet = 5000

        user_id, level, exp, points = self.economy_cog.get_global_user_data(ctx.author.id)
        if points < bet:
            await ctx.message.channel.send("Not enough coins for wager. You currently have {} coins.".format(points))
            return

        r = random.randint(0,100)
        if r < 50:
            coin = discord.File(os.path.join(self.src_dir,'img/heads.png'))
            if bet:
                await ctx.message.channel.send("Heads! You won {} coins.".format(bet), file=coin)
                await self.economy_cog.set_global_user_data(user_id, level, exp, points+bet)
            else:
                await ctx.message.channel.send("Heads", file=coin)
        else:
            coin = discord.File(os.path.join(self.src_dir,'img/tails.png'))
            if bet:
                await ctx.message.channel.send("Tails! You lost {} coins.".format(bet), file=coin)
                await self.economy_cog.set_global_user_data(user_id, level, exp, points-bet)
            else:
                await ctx.message.channel.send("Tails", file=coin)
        return
        
    @commands.command(name = 'roll')
    async def rollDie(self, ctx, arg=''):
        arg = int(arg or 1)

        channel = ctx.message.channel
        if arg >= 1 and arg <= 5:
            for x in range(arg):
                r = random.randint(1,6)
                die = discord.File(os.path.join(self.src_dir,'img/face{}.png' .format(r)))
                msg = await channel.send(file = die)
        elif arg < 1 or arg is None:
            r = random.randint(1,6)
            die = discord.File(os.path.join(self.src_dir,'img/face{}.png' .format(r)))
            msg = await channel.send(file = die)
        else:
            for x in range(5):
                r = random.randint(1,6)
                die = discord.File(os.path.join(self.src_dir,'img/face{}.png' .format(r)))
                msg = await channel.send(file = die)

def setup(bot):
    bot.add_cog(Gamble(bot))