import os
import datetime
import base64
import random
import re
import discord

from config import conf
from contextlib import closing
from discord.ext import tasks, commands

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = self.bot.get_cog('Database').db
        
        with closing(self.db.cursor()) as cursor:
            # Create `users` table if it does not exist
            cursor.execute('''CREATE TABLE IF NOT EXISTS users (id BIGINT PRIMARY KEY, level INTEGER, exp INTEGER, points INTEGER)''')
            # Create `transactions` 
            cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (src_id BIGINT, dest_id BIGINT, src_pts INTEGER, dest_pts INTEGER, amount INTEGER, ts timestamp)''')
            
        # Start the leaderboard update background task
        # self.lb_update.start()
            
    @commands.Cog.listener()
    async def on_message(self, message):
        """
        Event handler when user posts a message
        If not a command, add exp and currency to user's account
        """
        # Do nothing if author is self
        if message.author == self.bot.user:
            return
        # Do nothing if author is bot
        if message.author.bot:
            return

        # Do nothing if is a command
        if message.content.startswith("!") or message.content.startswith("?") or message.content.startswith("-"):
            return

        if "can i get an f" in message.content.lower() or "can i get a f" in message.content.lower():
            await message.add_reaction(emoji="🇫")
        await self.update_user_data(message)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """
        Event handler when user leaves the server
        Remove their database entry
        """
        current_month = datetime.date.today().strftime("%B_%Y")  
        with closing(self.db.cursor()) as cursor:
            cursor.execute('UPDATE users SET level=%s, exp=%s, points=%s WHERE id=%s', (1, 0, 0, member.id))
            self.db.commit()
            cursor.execute('UPDATE {} SET exp_this_month=%s, points_this_month=%s WHERE id=%s'.format(current_month), (1, 0, member.id))
            self.db.commit()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """
        Event handler when user leaves the server
        Add a new database entry
        """
        # Do nothing if author is bot
        if message.author.bot:
            return
        with closing(self.db.cursor()) as cursor:
            cursor.execute('INSERT INTO users VALUES (%s,%s,%s,%s)', (str(member.id),1,0,0))
            self.db.commit()

    # Commands
    @commands.command()
    async def dbcleanup(self, ctx):
        """
        Clean up the database and remove users that are not in the guild anymore
        """
        if ctx.message.author.id != conf["ADMIN_ID"]:
            return
        with closing(self.db.cursor()) as cursor:
            cursor.execute('SELECT id FROM users')
            query_response = cursor.fetchall()
        
        users_purged = 0
        current_month = datetime.date.today().strftime("%B_%Y")    
        
        for user_id in query_response:
            user_id = user_id[0]
            print(user_id, self.bot.get_user(user_id))
            if not self.bot.get_user(user_id):
                with closing(self.db.cursor()) as cursor:
                    cursor.execute('UPDATE users SET level=%s, exp=%s, points=%s WHERE id=%s', (1, 0, 0, user_id))
                    self.db.commit()
                with closing(self.db.cursor()) as cursor:
                    cursor.execute('UPDATE {} SET exp_this_month=%s, points_this_month=%s WHERE id=%s'.format(current_month), (1, 0, user_id))
                    self.db.commit()
                users_purged += 1
        await ctx.message.channel.send("{} users purged".format(users_purged))
        return  

    @commands.command()
    async def leaderboard(self, ctx):
        """
        -leaderboard -> posts the current exp/points leaderboard in the channel
        """
        channel = ctx.message.channel
        print("Sending leaderboard embed")
        
        # if not board or board.lower() == "global":
        # Fetch top players by exp and send embed
        with closing(self.db.cursor()) as cursor:
            cursor.execute('SELECT * FROM users ORDER BY exp DESC')
            query_response = cursor.fetchmany(5)
        embed = self.generate_global_exp_embed(query_response)
        await channel.send(embed=embed)

        # Fetch top players by points and send embed
        with closing(self.db.cursor()) as cursor:
            cursor.execute('SELECT * FROM users ORDER BY points DESC')
            query_response = cursor.fetchmany(5)
        embed = self.generate_global_pts_embed(query_response)
        await channel.send(embed=embed)
        # else:
        current_month = datetime.date.today().strftime("%B_%Y")    
        
        # # Fetch top players by exp and send embed
        # with closing(self.db.cursor()) as cursor:
        #     cursor.execute('SELECT * FROM {} ORDER BY exp_this_month DESC'.format(current_month))
        #     query_response = cursor.fetchmany(5)
        # embed = self.generate_monthly_exp_embed(query_response)
        # await channel.send(embed=embed)

        # # Fetch top players by points and send embed
        # with closing(self.db.cursor()) as cursor:
        #     cursor.execute('SELECT * FROM {} ORDER BY points_this_month DESC'.format(current_month))
        #     query_response = cursor.fetchmany(5)
        # embed = self.generate_monthly_pts_embed(query_response)
        # await channel.send(embed=embed)
            
    @commands.command()
    async def profile(self, ctx, user:discord.User=None):
        """
        -profile -> returns profile for the author of the message
        -profile @user -> returns profile for the specified user
        """
        if not user:
            # No user provided, return stats for self
            user = ctx.author

        with closing(self.db.cursor()) as cursor:
            cursor.execute('SELECT * FROM users WHERE id=%s', (str(user.id),) )
            query_response = cursor.fetchone()
        user_id, user_level, user_exp, user_points = query_response
        profile_str = "Level {} - {:,d} exp - {:,d} coins \n".format(conf["LEVEL_IMAGES"].get(user_level, user_level), user_exp, user_points)

        with closing(self.db.cursor()) as cursor:
            cursor.execute('SELECT * FROM gametime WHERE user_id=%s ORDER BY played DESC LIMIT 1', (str(user.id),))
            query_response = cursor.fetchone()

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

        # Try to get primary award
        # with closing(self.db.cursor()) as cursor:
        #     cursor.execute('SELECT * FROM users_awards_primary WHERE user_id=%s', (str(user.id),))
        #     award_response = cursor.fetchone()

        embed = discord.Embed(description=profile_str+game_str)
        embed.set_author(name=str(user), icon_url=str(user.avatar_url))
        # if award_response:
        #     user_id, award_name = award_response
        #     with closing(self.db.cursor()) as cursor:
        #         cursor.execute('SELECT * FROM awards WHERE award_id=%s', (award_name,))
        #         award_name, award_img = cursor.fetchone()
        #     award_img = base64.b64decode(award_img).decode()
        #     print(award_img)
        #     embed.set_thumbnail(url=award_img)
        await ctx.channel.send(embed=embed)

    @commands.command()
    async def givegold(self, ctx, user:discord.User=None, amount:int=None):
        """
        -givegold @user <amount> -> send gold to the mentioned user
        """
        amount = abs(amount)            

        if not user or not amount:
            await ctx.channel.send('You need to specify a user and amount. E.G. `-givegold @Auxilium 100`')
            return
        if user.id == ctx.author.id:
            await ctx.channel.send("You can't send gold to yourself.")
            return
        
        with closing(self.db.cursor()) as cursor:
            cursor.execute('SELECT * FROM users WHERE id=%s', (str(ctx.author.id),) )
            query_response = cursor.fetchone()
        auth_id, auth_level, auth_exp, auth_points = query_response

        if auth_points < int(amount):
            await ctx.channel.send("You don't have enough gold.")
            return

        with closing(self.db.cursor()) as cursor:
            cursor.execute('SELECT * FROM users WHERE id=%s', (str(user.id),) )
            query_response = cursor.fetchone()
        if not query_response:
            await ctx.channel.send("User doesn't exist.")
            return
        targ_id, targ_level, targ_exp, targ_points = query_response
        
        with closing(self.db.cursor()) as cursor:
            cursor.execute('UPDATE users SET level=%s, exp=%s, points=%s WHERE id=%s', (auth_level, auth_exp, auth_points-amount, str(auth_id)))
            self.db.commit()
            
            cursor.execute('UPDATE users SET level=%s, exp=%s, points=%s WHERE id=%s', (targ_level, targ_exp, targ_points+amount, str(targ_id)))
            self.db.commit()

        # #(src_id INTEGER, dest_id INTEGER, src_pts INTEGER, dest_pts INTEGER, amount INTEGER, ts timestamp)
        # self.db_cursor.execute('INSERT INTO transactions VALUES (%s,%s,%s,%s,%s,%s)', (auth_id, targ_id, auth_points, targ_points, amount, datetime.datetime.now()))
        # self.db.commit()
        
        await ctx.channel.send("Sent {} gold to {}. Your balance is now {}. Their balance is now {}.".format(amount, user.mention, auth_points-amount, targ_points+amount))
        return

    @tasks.loop(seconds=60)
    async def lb_update(self):
        print("Updating leaderboard")
        channel = self.bot.get_channel(conf["LEADERBOARD_CHANNEL"])
        if not channel:
            print("Batch update error in levels cog: channel {} not found.".format(conf["LEADERBOARD_CHANNEL"]))
            return
        
        # Get this month's exp leaderboard
        current_month = datetime.date.today().strftime("%B_%Y")
        with closing(self.db.cursor()) as cursor:
            cursor.execute('SELECT * FROM {} ORDER BY exp_this_month DESC'.format(current_month))
            query_response = cursor.fetchmany(5)
        if not query_response:
            print("No monthly exp leaders")
            return
        mo_exp_embed = self.generate_monthly_exp_embed(query_response)

        # Get this month's point leaderboard
        with closing(self.db.cursor()) as cursor:
            cursor.execute('SELECT * FROM {} ORDER BY points_this_month DESC'.format(current_month))
            query_response = cursor.fetchmany(5)
        if not query_response:
            print("No monthly point leaders")
            return
        mo_pts_embed = self.generate_monthly_pts_embed(query_response)

        # Fetch top players by exp
        with closing(self.db.cursor()) as cursor:
            cursor.execute('SELECT * FROM users ORDER BY exp DESC')
            query_response = cursor.fetchmany(5)
        glob_exp_embed = self.generate_global_exp_embed(query_response)

        # Fetch top players by points
        with closing(self.db.cursor()) as cursor:
            cursor.execute('SELECT * FROM users ORDER BY points DESC')
            query_response = cursor.fetchmany(5)
        glob_pts_embed = self.generate_global_pts_embed(query_response)
        
        embeds = [mo_pts_embed, mo_exp_embed, glob_pts_embed, glob_exp_embed]
        
        # Get the last message in the channel
        messages = await channel.history(limit=4).flatten()
        # If no messages exist, send the message. Otherwise edit existing messages
        if not messages or len(messages) < len(embeds):
            for embed in embeds:
                await channel.send(embed=embed)
        else:
            for i, embed in enumerate(embeds):
                await messages[i].edit(embed=embeds[i])
        
    # Util functions
    def get_monthly_user_data(self, user_id):
        current_month = datetime.date.today().strftime("%B_%Y")
        with closing(self.db.cursor()) as cursor:
            cursor.execute('SELECT * FROM {} WHERE id=%s'.format(current_month), (user_id, ))
            query_response = cursor.fetchone()
        if not query_response:
            # Add new user to table if they do not exist
            query_response = (user_id, 0, 0)
            with closing(self.db.cursor()) as cursor:
                cursor.execute('INSERT INTO {} VALUES (%s,%s,%s)'.format(current_month), query_response)
                self.db.commit()
        return query_response

    def get_global_user_data(self, user_id):
        with closing(self.db.cursor()) as cursor:
            cursor.execute('SELECT * FROM users WHERE id=%s', (user_id,) )
            query_response = cursor.fetchone()
        # Add new user to table if they do not exist
        if not query_response:
            # Add new user to table if they do not exist
            query_response = (user_id, 1, 0, 0)
            with closing(self.db.cursor()) as cursor:
                cursor.execute('INSERT INTO users VALUES (%s,%s,%s,%s)', query_response)
                self.db.commit()
        return query_response

    async def set_global_user_data(self, user_id, user_level, user_exp, user_points):
        with closing(self.db.cursor()) as cursor:
            cursor.execute('UPDATE users SET level=%s, exp=%s, points=%s WHERE id=%s', (user_level, user_exp, user_points, user_id))
            self.db.commit()
        return

    async def set_monthly_user_data(self, user_id, user_exp, user_points):
        current_month = datetime.date.today().strftime("%B_%Y")
        with closing(self.db.cursor()) as cursor:
            cursor.execute('UPDATE {} SET exp_this_month=%s, points_this_month=%s WHERE id=%s'.format(current_month), (user_exp, user_points, user_id))
            self.db.commit()
        return

    async def update_user_data(self, message):
        user_id, user_level, user_exp, user_points = self.get_global_user_data(str(message.author.id))
        _, user_exp_m, user_points_m = self.get_monthly_user_data(str(message.author.id))
        
        # Award random points between 1 to 10*user_level
        points = random.randint(1, 10*user_level)

        # Calculate exp to award based on length of message
        # Remove emojis
        message_str = re.sub('<[^>]+>', '', message.content).strip()
        # Remove links
        if "http" in message_str:
            message_str = " ".join([word for word in message_str.split(" ") if not word.startswith("http")])
        exp = float(conf["EXP_PER_CHAR"]) * len(message_str)

        # Calculate exp needed for next level. if a level occurs, send a message
        next_level_exp = 150 * ((user_level+1)**2) - (150 * (user_level+1))
        if user_exp > next_level_exp:
            user_level += 1
            await message.channel.send('{} reached level {}'.format(message.author.mention, conf["LEVEL_IMAGES"].get(user_level, user_level)))

        await self.set_global_user_data(user_id, user_level, user_exp+exp, user_points+points)
        await self.set_monthly_user_data(user_id, user_exp_m+exp, user_points_m+points)
        return
    
    def generate_global_exp_embed(self, query_response):
        embed = discord.Embed(title="Most exp on the server:", color=0x0092ff)
        embed.set_thumbnail(url="https://vignette.wikia.nocookie.net/wowwiki/images/2/2f/Achievement_doublejeopardy.png")
        for user_info in query_response:
            user_id, user_level, user_exp, user_points = user_info
            embed.add_field(name="{} {}".format(conf["LEVEL_IMAGES"].get(user_level, user_level), self.bot.get_user(user_id).name), 
                            value="{:,d} exp".format(user_exp), 
                            inline=False)
        return embed

    def generate_global_pts_embed(self, query_response):
        embed = discord.Embed(title="Most coins on the server:", color=0x0092ff)
        embed.set_thumbnail(url="https://vignette.wikia.nocookie.net/wowwiki/images/c/c4/Inv_misc_coin_02.png")
        for user_info in query_response:
            user_id, user_level, user_exp, user_points = user_info
            embed.add_field(name="{} {}".format(conf["LEVEL_IMAGES"].get(user_level, user_level), self.bot.get_user(user_id).name), 
                            value="{:,d} coins".format(user_points), 
                            inline=False)
        return embed

    def generate_monthly_exp_embed(self, query_response):
        embed = discord.Embed(title="Most exp gained this month:", color=0x0092ff)
        embed.set_thumbnail(url="https://vignette.wikia.nocookie.net/wowwiki/images/2/2f/Achievement_doublejeopardy.png")
        for user_info in query_response:
            user_id, user_exp, user_points = user_info
            # Monthly leaderboard doesn't have user level, so fetch from `users` table
            with closing(self.db.cursor()) as cursor:
                cursor.execute('SELECT level FROM users WHERE id=%s', (user_id,) )
                user_level = cursor.fetchone()[0]
            embed.add_field(name="{} {}".format(conf["LEVEL_IMAGES"].get(user_level, user_level), self.bot.get_user(user_id).name), 
                            value="{:,d} exp".format(user_exp), 
                            inline=False)
        return embed

    def generate_monthly_pts_embed(self, query_response):
        embed = discord.Embed(title="Most coins gained this month:", color=0x0092ff)
        embed.set_thumbnail(url="https://vignette.wikia.nocookie.net/wowwiki/images/c/c4/Inv_misc_coin_02.png")
        for user_info in query_response:
            user_id, user_exp, user_points = user_info
            # Monthly leaderboard doesn't have user level, so fetch from `users` table
            with closing(self.db.cursor()) as cursor:
                cursor.execute('SELECT level FROM users WHERE id=%s', (user_id,) )
                user_level = cursor.fetchone()[0]
            embed.add_field(name="{} {}".format(conf["LEVEL_IMAGES"].get(user_level, user_level), self.bot.get_user(user_id).name), 
                            value="{:,d} coins".format(user_points), 
                            inline=False)
        return embed


def setup(bot):
    bot.add_cog(Economy(bot))
