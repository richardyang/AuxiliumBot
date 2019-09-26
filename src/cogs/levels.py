import os
import datetime
import sqlite3
import config

import discord
from discord.ext import tasks, commands

class Levels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Open connection to SQLite DB
        src_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))
        self.db = sqlite3.connect(os.path.join(src_dir, config.DB_NAME))
        self.db_cursor = self.db.cursor()
        # Create `users` table if it does not exist
        self.db_cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, level INTEGER, exp INTEGER, points INTEGER)''')
        # Create `monthly stats` 
        self.current_month = datetime.date.today().strftime("%B_%Y") # Format current time to Month-Year
        self.db_cursor.execute('''CREATE TABLE IF NOT EXISTS {} (id INTEGER PRIMARY KEY, exp_this_month INTEGER, points_this_month INTEGER)'''.format(self.current_month))
        
        # Start the leaderboard update background task
        self.lb_update.start()
            
    @commands.Cog.listener()
    async def on_message(self, message):
        # Do nothing if author is self
        if message.author == self.bot.user:
            return
        # Do nothing if author is bot
        if message.author.bot:
            return

        await self.update_user_data(message)
        await self.update_monthly_exp(message)

    async def update_monthly_exp(self, message):
        # Fetch user info from database
        current_month = datetime.date.today().strftime("%B_%Y")
        self.db_cursor.execute('SELECT * FROM {} WHERE id=?'.format(current_month), (str(message.author.id), ))
        query_response = self.db_cursor.fetchone()
        
        # Add new user to DB if they do not exist
        if not query_response:
            self.db_cursor.execute('INSERT INTO {} VALUES (?,?,?)'.format(current_month), (str(message.author.id), 0, 0))
            self.db.commit()
            query_response = (str(message.author.id), 0, 0)
        
        # Unpack the results and award exp/points
        user_id, user_exp, user_points = query_response
        user_exp += config.EXP_PER_MSG
        user_points += config.PTS_PER_CHAR * len(message.content.split(" ")) + 5 * int(len(message.attachments))

        # Update the DB
        self.db_cursor.execute('UPDATE {} SET exp_this_month=?, points_this_month=? WHERE id=?'.format(current_month), (user_exp, user_points, str(message.author.id)))
        self.db.commit()
    
    async def update_user_data(self, message):
        # Fetch user info from database
        self.db_cursor.execute('SELECT * FROM users WHERE id=?', (str(message.author.id),) )
        query_response = self.db_cursor.fetchone()
        
        # Add new user to DB if they do not exist
        if not query_response:
            self.db_cursor.execute('INSERT INTO users VALUES (?,?,?,?)', (str(message.author.id), 1, 0, 0))
            self.db.commit()
            query_response = (str(message.author.id), 1, 0, 0)
        
        # Unpack the results and award exp/points
        user_id, user_level, user_exp, user_points = query_response
        user_exp += config.EXP_PER_MSG
        user_points += config.PTS_PER_CHAR * len(message.content.split(" ")) + 5 * int(len(message.attachments))

        # Calculate actual level. If a level up occurs, send a message
        actual_level = int(user_exp / 100 + 1)
        if user_level < actual_level:
            user_level = actual_level
            await message.channel.send('{} reached level {}'.format(message.author.mention, config.LEVEL_IMAGES[user_level]))
        
        # Update the DB
        self.db_cursor.execute('UPDATE users SET level=?, exp=?, points=? WHERE id=?', (user_level, user_exp, user_points, str(message.author.id)))
        self.db.commit()

    # Commands
    @commands.command()
    async def leaderboard(self, ctx):
        channel = ctx.message.channel
        print("Sending leaderboard embed")
        
        # Get this month's leaderboard
        current_month = datetime.date.today().strftime("%B_%Y")
        self.db_cursor.execute('SELECT * FROM {} WHERE id!=? ORDER BY exp_this_month DESC'.format(current_month), (str(config.ADMIN_ID),))
        query_response = self.db_cursor.fetchmany(5)

        # Format results as an embed
        embed = self.generate_exp_embed(query_response)
        await channel.send(embed=embed)
    
    # Background Tasks
    @tasks.loop(seconds=60)
    async def lb_update(self):
        print("Updating leaderboard")
        channel = self.bot.get_channel(config.LEADERBOARD_CHANNEL)
        if not channel:
            print("Batch update error in levels cog: channel {} not found.".format(config.LEADERBOARD_CHANNEL))
            return
        
        # Get this month's exp leaderboard
        current_month = datetime.date.today().strftime("%B_%Y")
        self.db_cursor.execute('SELECT * FROM {} WHERE id!=? ORDER BY exp_this_month DESC'.format(current_month), (str(config.ADMIN_ID),))
        query_response = self.db_cursor.fetchmany(5)
        exp_embed = self.generate_exp_embed(query_response)

        # Get this month's point leaderboard
        self.db_cursor.execute('SELECT * FROM {} WHERE id!=? ORDER BY points_this_month DESC'.format(current_month), (str(config.ADMIN_ID),))
        query_response = self.db_cursor.fetchmany(5)
        pts_embed = self.generate_pts_embed(query_response)

        # Get the last message in the channel
        messages = await channel.history(limit=2).flatten()
        # If no messages exist, send the message. Otherwise edit existing messages
        if not messages:
            await channel.send(embed=exp_embed)
            await channel.send(embed=pts_embed)
        else:
            await messages[1].edit(embed=exp_embed)
            await messages[0].edit(embed=pts_embed)
    
    def generate_exp_embed(self, query_response):
        embed = discord.Embed(title="Most exp gained this month:", color=0x0092ff)
        embed.set_thumbnail(url="https://vignette.wikia.nocookie.net/wowwiki/images/2/2f/Achievement_doublejeopardy.png")
        # embed.set_footer(text="Last updated 1 minute ago", icon_url="https://cdn.discordapp.com/app-icons/619670204506701829/e0ca67b591d30e8b54c8044f0e702e4c.png")
        for user_info in query_response:
            user_id, user_exp, user_points = user_info
            # Monthly leaderboard doesn't have user level, so fetch from `users` table
            self.db_cursor.execute('SELECT level FROM users WHERE id=?', (user_id,) )
            user_level = self.db_cursor.fetchone()[0]
            embed.add_field(name="{} {}".format(config.LEVEL_IMAGES[user_level], self.bot.get_user(user_id).name), 
                            value="{} exp".format(user_exp), 
                            inline=False)
        return embed

    def generate_pts_embed(self, query_response):
        embed = discord.Embed(title="Most coins gained this month:", color=0xdadada)
        embed.set_thumbnail(url="https://vignette.wikia.nocookie.net/wowwiki/images/c/c4/Inv_misc_coin_02.png")
        # embed.set_footer(text="Last updated 1 minute ago", icon_url="https://cdn.discordapp.com/app-icons/619670204506701829/e0ca67b591d30e8b54c8044f0e702e4c.png")
        for user_info in query_response:
            user_id, user_exp, user_points = user_info
            # Monthly leaderboard doesn't have user level, so fetch from `users` table
            self.db_cursor.execute('SELECT level FROM users WHERE id=?', (user_id,) )
            user_level = self.db_cursor.fetchone()[0]
            embed.add_field(name="{} {}".format(config.LEVEL_IMAGES[user_level], self.bot.get_user(user_id).name), 
                            value="{} coins".format(user_points), 
                            inline=False)
        return embed

def setup(bot):
    bot.add_cog(Levels(bot))