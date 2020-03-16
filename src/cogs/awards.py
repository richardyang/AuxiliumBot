import os
import sqlite3
import datetime
import base64
import discord

from config import conf
from contextlib import closing
from discord.ext import tasks, commands

class Awards(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        self.db = self.bot.get_cog('Database').db
        with closing(self.db.cursor()) as cursor:    
            # Create `award` dbs
            cursor.execute('''CREATE TABLE IF NOT EXISTS users_awards (user_id BIGINT, award_id VARCHAR(3072))''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS awards (award_id VARCHAR(3072) PRIMARY KEY, award_img VARCHAR(3072))''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS users_awards_primary (user_id BIGINT PRIMARY KEY, award_id VARCHAR(3072))''')
        
        self.background_tasks.start()

    @commands.command()
    async def giveaward(self, ctx, user:discord.User, award_name):
        if ctx.author.id != config.ADMIN_ID:
            await ctx.channel.send("{}, you don't have permission to issue awards.".format(ctx.author.mention))
            return
        
        await self._giveaward(str(user.id), str(award_name))
        print("Award {} given to {}".format(award_name, user.name))
                
    @commands.command()
    async def addaward(self, ctx, award_name, award_img):
        if ctx.author.id != config.ADMIN_ID:
            await ctx.channel.send("{}, you don't have permission to add awards.".format(ctx.author.mention))
            return

        await self._createaward(str(award_name), str(award_img))
        print("Award {} added".format(award_name))
        return

    # @commands.command()
    # async def deleteaward(self, ctx, award_name):
    #     if ctx.author.id != config.ADMIN_ID:
    #         await ctx.channel.send("{}, you don't have permission to remove awards.".format(ctx.author.mention))
    #         return

    #     self.awards_list_db.delete(award_name)
    #     await ctx.channel.send("Award {} deleted.".format(award_name))
    #     return

    async def _giveaward(self, user_id, award_name):
        award_name = base64.b64encode(award_name.encode())
        # TODO check if award is already in DB
        with closing(self.db.cursor()) as cursor:   
            cursor.execute('''INSERT INTO users_awards VALUES (%s,%s)''', (user_id, award_name))
            self.db.commit()

            # Check if user has a primary award, otherwise set this as primary award
            cursor.execute('''SELECT * FROM users_awards_primary WHERE user_id=%s''', (user_id,))
            query_response = cursor.fetchone()
        
            if not query_response:
                cursor.execute('''INSERT INTO users_awards_primary VALUES (%s,%s)''', (user_id, award_name))
                self.db.commit()

    async def _createaward(self, award_name, award_img):
        award_name = base64.b64encode(award_name.encode())
        award_img = base64.b64encode(award_img.encode())

        # TODO check if award is already in DB
        with closing(self.db.cursor()) as cursor:   
            cursor.execute('''INSERT INTO awards VALUES (%s,%s)''', (award_name, award_img))
            self.db.commit()
     
    @tasks.loop(seconds=60)
    async def background_tasks(self):
        # Check if bot is connected to server first
        if not self.bot.get_user(config.ADMIN_ID):
            return
        current_month = datetime.date.today().strftime("%B_%Y") # Format current time to Month-Year

        # Identify a month change occured by checking if the current month's table exists
        with closing(self.db.cursor()) as cursor:   
            # cursor.execute('''SELECT name FROM auxilium-db WHERE type='table' AND name=%s''', (current_month,))
            cursor.execute('''SHOW TABLES LIKE %s''', (current_month,))
            table_exists = cursor.fetchall()
    
        if not table_exists:
            print("="*10)
            # Create new table for this month
            with closing(self.db.cursor()) as cursor:   
                cursor.execute('''CREATE TABLE IF NOT EXISTS {} (id BIGINT PRIMARY KEY, exp_this_month INTEGER, points_this_month INTEGER)'''.format(current_month))
            
            yesterday = datetime.date.today() - datetime.timedelta(days=7)
            last_month = yesterday.strftime("%B_%Y")

            print("Previous month: {}".format(last_month))
            print("New month: {}".format(current_month))

            # Award leaderboard winner from last month
            # Create award
            award_name = last_month.replace("_", " ") + " Champion"
            await self._createaward(award_name, "https://www.pollux.fun/build/flairs/top/default.png")
            print("New award created: {}".format(award_name))
            
            # Get the leader
            with closing(self.db.cursor()) as cursor:   
                cursor.execute('SELECT * FROM {} WHERE id!=%s ORDER BY exp_this_month DESC'.format(last_month), (str(config.ADMIN_ID),))
                query_response = cursor.fetchone()
            user_id, _, _ = query_response
            await self._giveaward(user_id, award_name)
            print("Previous champion: {}".format(self.bot.get_user(user_id).name))
        
        return



def setup(bot):
    bot.add_cog(Awards(bot))