import os
import base64
import sqlite3
import datetime
import config
import discord
from discord.ext import tasks, commands

class Tracker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Open connection to SQLite DB
        src_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))
        self.db = sqlite3.connect(os.path.join(src_dir, config.DB_NAME+".db"))
        self.db_cursor = self.db.cursor()
        # Create `gametime` table if it does not exist
        self.db_cursor.execute('''CREATE TABLE IF NOT EXISTS gametime (user_id INTEGER, app_id VARCHAR(500), played INTEGER)''')
        self.get_activity.start()

    @commands.command()
    async def topgames(self, ctx, user:discord.User=None):
        """
        -topgames -> returns top games (up to 5) for the author of the message
        -topgames @user -> returns top games (up to 5) for the specified user
        """
        if not user:
            # No user provided, return stats for self
            user_id = ctx.author.id
            who = "Your" # Used for formatting the response
        else:
            user_id = user.id
            who = "{}'s".format(user.display_name)

        # Get data from db
        self.db_cursor.execute('SELECT * FROM gametime WHERE user_id=? ORDER BY played DESC LIMIT 5', (str(user_id),))
        query_response = self.db_cursor.fetchall()
        # If no game data found in db, send a response
        if not query_response:
            if not user:
                await ctx.channel.send("{}, I don't have any data on you. Check to see if you've enabled game activity: Discord Setting -> Game Activity -> Select 'Display currently running game as a status message'.".format(ctx.author.mention))
            else: 
                await ctx.channel.send("{}, I don't have any data on {}.".format(ctx.author.mention, user.display_name))
            return

        response = ""
        for i, game in enumerate(query_response):
            user_id, app_id, played = game

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

            response += "{}. {} - {}{} \n".format(i+1, base64.b64decode(app_id).decode(), splayed_hours, splayed_mins)
        
        embed = discord.Embed(title="{} top {} games:".format(who, len(query_response)), description=response, color=0x0092ff)        
        await ctx.channel.send(embed=embed)

    @commands.command()
    async def guildtopgames(self, ctx):
        """
        -guildtopgames -> returns the top games (up to 5) for the entire guild
        """
        self.db_cursor.execute('SELECT app_id, SUM(played) played_sum FROM gametime GROUP BY app_id ORDER BY played_sum DESC LIMIT 5')
        query_response = self.db_cursor.fetchall()

        response = ""
        for i, game in enumerate(query_response):
            app_id, played = game
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

            response += "{}. {} - {}{} \n".format(i+1, base64.b64decode(app_id).decode(), splayed_hours, splayed_mins)
        
        embed = discord.Embed(title="The guild's top {} games:".format(len(query_response)), description=response, color=0x0092ff)        
        await ctx.channel.send(embed=embed)
        
    @tasks.loop(seconds=60)
    async def get_activity(self):
        """
        Get all online users' activity every minute and store in db
        """
        logged_players = []
        for m in self.bot.get_all_members():
            # Skip all bots, offline players, and duplicates
            if m.bot or str(m.status) == "offline" or m.id in logged_players:
                continue
            
            # Check if the user is currently in any activities and log to db
            if m.activities:
                # Base64 encode the game name so that it can be easily stored in db
                await self.update_db(m.id, base64.b64encode(m.activities[0].name.encode()))

        return

    async def update_db(self, user_id, app_id):
        # Fetch user info from database
        self.db_cursor.execute('SELECT * FROM gametime WHERE user_id=? AND app_id=?', (user_id, app_id))
        query_response = self.db_cursor.fetchone()
        
        if not query_response:
            self.db_cursor.execute('INSERT INTO gametime VALUES (?,?,?)', (user_id, app_id, 1))
            self.db.commit()
            return
        
        user_id, app_id, gametime = query_response
        self.db_cursor.execute('UPDATE gametime SET played=? WHERE user_id=? AND app_id=?', (str(gametime + 1), user_id, app_id))
        self.db.commit()
        return

def setup(bot):
    bot.add_cog(Tracker(bot))