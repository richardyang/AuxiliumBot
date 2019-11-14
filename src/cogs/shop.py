import config
import pymysql
import discord
from discord.ext import tasks, commands

class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = self.bot.get_cog('Database').db
        self.economy_cog = self.bot.get_cog('Economy')
        self.current_bid = 0
    
    @commands.command()
    async def buystatus(self, ctx, amount:int, *status):
        channel = ctx.message.channel
        if not amount or not status:
            await channel.send("Usage: `-buystatus <amount> <message>`. Specify 'playing', 'streaming', 'listening' or 'watching' in message, or 'playing' will be used by default.")
            return
        status = " ".join(status)
        
        if amount <= self.current_bid:
            await channel.send("The current bid for the bot status is {0}, you need to specify an amount greater than that.".format(self.current_bid))
            return
        
        user_id, user_level, user_exp, user_points = self.economy_cog.get_global_user_data(ctx.author.id)
        if amount > user_points:
            await channel.send("You don't have enough coins for this transaction. Your available balance is {0}".format(user_points))
            return
        
        await channel.send("Purchase successful! Setting the bot status to: '{0}'. The current bid is now {1} coins.".format(status, amount))
        self.current_bid = amount
        await self.economy_cog.set_global_user_data(user_id, user_level, user_exp, user_points-amount)

        if status.lower().startswith("streaming"):
            await self.bot.change_presence(activity=discord.Streaming(name=status[len("streaming"):].strip(), url="https://www.twitch.tv/auxguild"))
        elif status.lower().startswith("listening to"):
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=status[len("listening to"):].strip()))
        elif status.lower().startswith("listening"):
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=status[len("listening"):].strip()))
        elif status.lower().startswith("watching"):
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status[len("watching"):].strip()))
        elif status.lower().startswith("playing"):
            await self.bot.change_presence(activity=discord.Game(name=status[len("playing"):].strip()))
        else:
            await self.bot.change_presence(activity=discord.Game(name=status))
        return            

def setup(bot):
    bot.add_cog(Shop(bot))
    
