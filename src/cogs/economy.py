import os
import datetime
import base64
import sqlite3
import config

import discord
from discord.ext import tasks, commands

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Open connection to SQLite DB
        src_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))
        self.db = sqlite3.connect(os.path.join(src_dir, config.DB_NAME+".db"))
        self.db_cursor = self.db.cursor()
        # Create `users` table if it does not exist
        self.db_cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, level INTEGER, exp INTEGER, points INTEGER)''')
        # Create `monthly stats` 
        self.current_month = datetime.date.today().strftime("%B_%Y") # Format current time to Month-Year
        self.db_cursor.execute('''CREATE TABLE IF NOT EXISTS {} (id INTEGER PRIMARY KEY, exp_this_month INTEGER, points_this_month INTEGER)'''.format(self.current_month))
        # Create `transactions` 
        self.db_cursor.execute('''CREATE TABLE IF NOT EXISTS trx (src_id INTEGER, dest_id INTEGER, src_pts INTEGER, dest_pts INTEGER, amount INTEGER, ts timestamp)''')

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

        # Do nothing if is a command
        if message.content.startswith("!") or message.content.startswith("?") or message.content.startswith("-"):
            return

        await self.update_user_data(message)
        await self.update_monthly_data(message)

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

    @commands.command()
    async def profile(self, ctx, user:discord.User=None):
        """
        -profile -> returns profile for the author of the message
        -profile @user -> returns profile for the specified user
        """
        if not user:
            # No user provided, return stats for self
            user = ctx.author

        self.db_cursor.execute('SELECT * FROM users WHERE id=?', (str(user.id),) )
        query_response = self.db_cursor.fetchone()
        user_id, user_level, user_exp, user_points = query_response
        profile_str = "Level {} - {:,d} exp - {:,d} coins \n".format(config.LEVEL_IMAGES[user_level], user_exp, user_points)

        self.db_cursor.execute('SELECT * FROM gametime WHERE user_id=? ORDER BY played DESC LIMIT 1', (str(user.id),))
        query_response = self.db_cursor.fetchone()
        if query_response:
            user_id, app_id, played = query_response
            # String formatting for response
            played_hours = played // 60
            played_mins = played % 60
            if played_hours == 1:
                splayed_hours = "1 hour and "
            elif played_hours == 0:
                splayed_hours = ""
            else:
                splayed_hours = str(played_hours) + " hours and "

            if played_mins == 1:
                splayed_mins = "1 minute"
            else:
                splayed_mins = str(played_mins) + " minutes"
            game_str = "Top game: {} - {}{}".format(base64.b64decode(app_id).decode(), splayed_hours, splayed_mins)
        else:
            game_str = ""

        embed = discord.Embed(description=profile_str+game_str)
        embed.set_author(name=str(user), icon_url=str(user.avatar_url))
        await ctx.channel.send(embed=embed)

    @commands.command()
    async def givegold(self, ctx, user:discord.User=None, amount:int=None):
        if not user or not amount:
            await ctx.channel.send('You need to specify a user and amount. E.G. `-givegold @Auxilium 100`')
            return
        if user.id == ctx.author.id:
            await ctx.channel.send("You can't send gold to yourself.")
            return
        
        self.db_cursor.execute('SELECT * FROM users WHERE id=?', (str(ctx.author.id),) )
        query_response = self.db_cursor.fetchone()
        auth_id, auth_level, auth_exp, auth_points = query_response

        if auth_points < int(amount):
            await ctx.channel.send("You don't have enough gold.")
            return

        self.db_cursor.execute('SELECT * FROM users WHERE id=?', (str(user.id),) )
        query_response = self.db_cursor.fetchone()
        if not query_response:
            await ctx.channel.send("User doesn't exist.")
            return
        targ_id, targ_level, targ_exp, targ_points = query_response

        self.db_cursor.execute('UPDATE users SET level=?, exp=?, points=? WHERE id=?', (auth_level, auth_exp, auth_points-amount, str(auth_id)))
        self.db.commit()

        self.db_cursor.execute('UPDATE users SET level=?, exp=?, points=? WHERE id=?', (targ_level, targ_exp, targ_points+amount, str(targ_id)))
        self.db.commit()

        #(src_id INTEGER, dest_id INTEGER, src_pts INTEGER, dest_pts INTEGER, amount INTEGER, ts timestamp)
        self.db_cursor.execute('INSERT INTO trx VALUES (?,?,?,?,?,?)', (auth_id, targ_id, auth_points, targ_points, amount, datetime.datetime.now()))
        self.db.commit()
        
        await ctx.channel.send("Sent {} gold to {}. Your balance is now: {}. Their balance is now: {}".format(amount, user.mention, auth_points-amount, targ_points+amount))
        return
    

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
    
    # Util functions
    async def update_user_data(self, message):
        # Fetch user info from database
        self.db_cursor.execute('SELECT * FROM users WHERE id=?', (str(message.author.id),) )
        query_response = self.db_cursor.fetchone()
        
        # Add new user to DB if they do not exist
        if not query_response:
            user_points = config.PTS_PER_CHAR * len(message.content.split(" ")) + 5 * int(len(message.attachments))
            self.db_cursor.execute('INSERT INTO users VALUES (?,?,?,?)', (str(message.author.id), 1, config.EXP_PER_MSG, user_points))
            self.db.commit()
            return
        
        # Unpack the results and award exp/points
        user_id, user_level, user_exp, user_points = query_response
        # user_exp += config.EXP_PER_MSG * len(message.content) + 5 * int(len(message.attachments))
        user_exp += 5
        user_points += config.PTS_PER_CHAR * len(message.content) + 5 * int(len(message.attachments))

        # Calculate actual level. If a level up occurs, send a message
        actual_level = min(60, int(user_exp / 100 + 1))
        if user_level < actual_level:
            user_level = actual_level
            await message.channel.send('{} reached level {}'.format(message.author.mention, config.LEVEL_IMAGES[user_level]))
        
        # Update the DB
        self.db_cursor.execute('UPDATE users SET level=?, exp=?, points=? WHERE id=?', (user_level, user_exp, user_points, str(message.author.id)))
        self.db.commit()

    async def update_monthly_data(self, message):
        # Fetch user info from database
        current_month = datetime.date.today().strftime("%B_%Y")
        self.db_cursor.execute('SELECT * FROM {} WHERE id=?'.format(current_month), (str(message.author.id), ))
        query_response = self.db_cursor.fetchone()
        
        # Add new user to DB if they do not exist
        if not query_response:
            user_points = config.PTS_PER_CHAR * len(message.content.split(" ")) + 5 * int(len(message.attachments))
            self.db_cursor.execute('INSERT INTO {} VALUES (?,?,?)'.format(current_month), (str(message.author.id), config.EXP_PER_MSG, user_points))
            self.db.commit()
            return
        
        # Unpack the results and award exp/points
        user_id, user_exp, user_points = query_response
        # user_exp += config.EXP_PER_MSG * len(message.content) + 5 * int(len(message.attachments))
        user_exp += 5
        user_points += config.PTS_PER_CHAR * len(message.content) + 5 * int(len(message.attachments))

        # Update the DB
        self.db_cursor.execute('UPDATE {} SET exp_this_month=?, points_this_month=? WHERE id=?'.format(current_month), (user_exp, user_points, str(message.author.id)))
        self.db.commit()

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
                            value="{:,d} exp".format(user_exp), 
                            inline=False)
        return embed

    def generate_pts_embed(self, query_response):
        embed = discord.Embed(title="Most coins gained this month:", color=0x0092ff)
        embed.set_thumbnail(url="https://vignette.wikia.nocookie.net/wowwiki/images/c/c4/Inv_misc_coin_02.png")
        # embed.set_footer(text="Last updated 1 minute ago", icon_url="https://cdn.discordapp.com/app-icons/619670204506701829/e0ca67b591d30e8b54c8044f0e702e4c.png")
        for user_info in query_response:
            user_id, user_exp, user_points = user_info
            # Monthly leaderboard doesn't have user level, so fetch from `users` table
            self.db_cursor.execute('SELECT level FROM users WHERE id=?', (user_id,) )
            user_level = self.db_cursor.fetchone()[0]
            embed.add_field(name="{} {}".format(config.LEVEL_IMAGES[user_level], self.bot.get_user(user_id).name), 
                            value="{:,d} coins".format(user_points), 
                            inline=False)
        return embed


def setup(bot):
    bot.add_cog(Economy(bot))