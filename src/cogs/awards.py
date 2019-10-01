import os
import config
import sqlite3
import datetime
import base64

import discord
from discord.ext import tasks, commands

class Awards(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Open connection to SQLite DB
        src_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))
        self.db = sqlite3.connect(os.path.join(src_dir, config.DB_NAME+".db"))
        self.db_cursor = self.db.cursor()
        # Create `award` dbs
        self.db_cursor.execute('''CREATE TABLE IF NOT EXISTS users_awards (user_id INTEGER, award_id VARCHAR(5000))''')
        self.db_cursor.execute('''CREATE TABLE IF NOT EXISTS awards (award_id VARCHAR(5000) PRIMARY KEY, award_img VARCHAR(5000))''')
        self.db_cursor.execute('''CREATE TABLE IF NOT EXISTS users_awards_primary (user_id INTEGER PRIMARY KEY, award_id VARCHAR(5000))''')
        
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
        self.db_cursor.execute('''INSERT INTO users_awards VALUES (?,?)''', (user_id, award_name))
        self.db.commit()

        # Check if user has a primary award, otherwise set this as primary award
        self.db_cursor.execute('''SELECT * FROM users_awards_primary WHERE user_id=?''', (user_id,))
        query_response = self.db_cursor.fetchone()
        if not query_response:
            self.db_cursor.execute('''INSERT INTO users_awards_primary VALUES (?,?)''', (user_id, award_name))
            self.db.commit()

    async def _createaward(self, award_name, award_img):
        award_name = base64.b64encode(award_name.encode())
        award_img = base64.b64encode(award_img.encode())

        # TODO check if award is already in DB
        
        self.db_cursor.execute('''INSERT INTO awards VALUES (?,?)''', (award_name, award_img))
        self.db.commit()
     
    @tasks.loop(seconds=30)
    async def background_tasks(self):
        current_month = datetime.date.today().strftime("%B_%Y") # Format current time to Month-Year

        # Identify a month change occured by checking if the current month's table exists
        table_exists = self.db_cursor.execute('''SELECT name FROM sqlite_master WHERE type='table' AND name=?''', (current_month,))
        table_exists = self.db_cursor.fetchall()
    
        if not table_exists:
            print("="*10)
            # Create new table for this month
            self.db_cursor.execute('''CREATE TABLE IF NOT EXISTS {} (id INTEGER PRIMARY KEY, exp_this_month INTEGER, points_this_month INTEGER)'''.format(current_month))
            
            yesterday = datetime.date.today() - datetime.timedelta(days=1)
            last_month = yesterday.strftime("%B_%Y")

            print("Previous month: {}".format(last_month))
            print("New month: {}".format(current_month))

            # Award leaderboard winner from last month
            # Create award
            award_name = last_month.replace("_", " ") + " Champion"
            await self._createaward(award_name, "https://www.pollux.fun/build/flairs/top/default.png")
            print("New award created: {}".format(award_name))
            
            # Get the leader
            self.db_cursor.execute('SELECT * FROM {} WHERE id!=? ORDER BY exp_this_month DESC'.format(last_month), (str(config.ADMIN_ID),))
            query_response = self.db_cursor.fetchone()
            user_id, _, _ = query_response
            await self._giveaward(user_id, award_name)
            print("Previous champion: {}".format(self.bot.get_user(user_id).name))
        
        return



def setup(bot):
    bot.add_cog(Awards(bot))