import config
import pymysql
import discord
from discord.ext import tasks, commands

class Database(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = pymysql.connect(host=config.DB_HOST, port=config.DB_PORT, user=config.DB_USER, password=config.DB_PASS, db=config.DB_INST)

def setup(bot):
    bot.add_cog(Database(bot))
    