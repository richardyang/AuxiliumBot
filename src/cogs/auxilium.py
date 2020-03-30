import os
import random
import discord
import time
import pymysql
import json
import numpy as np

from config import conf
from contextlib import closing
from discord.ext import commands

class Auxilium(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.src_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))
        self.db = self.bot.get_cog('Database').db
        self.economy_cog = self.bot.get_cog("Economy")
    
    @commands.command()
    async def billy(self, ctx):
        print("Press F for Billy")
        channel = ctx.message.channel
        file = discord.File(os.path.join(self.src_dir, 'img/billy.gif'))
        msg = await channel.send("Press F to pay respects", file=file)
        await msg.add_reaction(emoji="🇫")

    
    @commands.command()
    async def ship(self, ctx, user1, user2=None):
        channel = ctx.message.channel
        if not user2:
            user2 = user1
            user1 = ctx.message.author.mention

        hash1 = int(abs(hash(str(user1))) % (10 ** 8) * 1.5)
        hash2 = abs(hash(str(user2))) % (10 ** 8)
        result = abs(hash1-hash2) % 100

        if result < 13:
            result_txt = "Awful 😭"
        elif 13 <= result < 26:
            result_txt = "Bad 😢"
        elif 26 <= result < 39:
            result_txt = "Pretty Low 🙁"
        elif 39 <= result < 52:
            result_txt = "Barely 😕"
        elif result == 69:
            result_txt = "( ͡° ͜ʖ ͡°)"
        elif 52 <= result < 65:
            result_txt = "Not Bad 🤔"
        elif 65 <= result < 78:
            result_txt = "Pretty Good 😄"
        elif 78 <= result < 91:
            result_txt = "Great 😊"
        elif 91 <= result < 100:
            result_txt = "Amazing 😘"
        else:
            result_txt = "PERFECT!! 😍"
        
        progress = "█" * (result//10 + 1) + " "*(10 - result//10)
        embed = discord.Embed(description="{}% [{}](https://auxilium.gg) {}".format(result, progress, result_txt), color=0xe882e8)
        
        await channel.send("❤️ COMPATIBILITY ❤️ \n 🔻 {0} \n 🔺 {1}".format(str(user1), str(user2), result, result_txt), embed=embed)


def setup(bot):
    bot.add_cog(Auxilium(bot))