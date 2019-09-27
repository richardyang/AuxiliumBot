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
        self.db = sqlite3.connect(os.path.join(src_dir, config.DB_NAME))
        self.db_cursor = self.db.cursor()
        # Create `gametime` table if it does not exist
        self.db_cursor.execute('''CREATE TABLE IF NOT EXISTS gametime (user_id INTEGER, app_id VARCHAR(500), played INTEGER)''')
        self.get_activity.start()

    @commands.command()
    async def mytopgames(self, ctx):
        self.db_cursor.execute('SELECT * FROM gametime WHERE user_id=? ORDER BY played DESC LIMIT 5', (str(ctx.author.id),))
        query_response = self.db_cursor.fetchall()
        if not query_response:
            await ctx.channel.send("{}, I don't have any data on you.".format(ctx.author.mention))

        response = ""
        for i, game in enumerate(query_response):
            user_id, app_id, played = game
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
        
        embed = discord.Embed(title="Your top {} games are:".format(len(query_response)), description=response, color=0x0092ff)        
        await ctx.channel.send(embed=embed)
        
    @tasks.loop(seconds=60)
    async def get_activity(self):
        online_players = {}
        for m in self.bot.get_all_members():
            if m.bot or str(m.status) == "offline" or m.id in online_players:
                continue
            
            if m.activities:
                game = None
                for a in m.activities:
                    if isinstance(a, discord.activity.Game) or isinstance(a, discord.activity.Activity):
                        game = a
                        break
                # No game found
                if not game:
                    continue
                online_players[m.id] = game.name

        for user_id, game_name in online_players.items():
            await self.update_db(user_id, base64.b64encode(game_name.encode()))
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