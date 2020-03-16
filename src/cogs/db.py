import os
import pymysql
import sqlite3
import discord

from config import conf
from discord.ext import tasks, commands

class Database(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        if conf["DB_TYPE"].lower().strip() == "mysql":
            self.db = pymysql.connect(host=conf["MYSQL_HOST"], user=conf["MYSQL_USER"], password=conf["MYSQL_PASS"], db=conf["MYSQL_DB"])
        else:
            src_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))
            self.db = sqlite3.connect(os.path.join(src_dir, "auxilium.db"))        

def setup(bot):
    bot.add_cog(Database(bot))
    
