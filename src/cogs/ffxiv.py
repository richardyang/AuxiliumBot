import pymysql
import discord
import requests
import string

from config import conf
from contextlib import closing
from discord.ext import tasks, commands

class FFXIV(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = self.bot.get_cog('Database').db
        self.economy_cog = self.bot.get_cog('Economy')

        with closing(self.db.cursor()) as cursor:
            # Create `users` table if it does not exist
            cursor.execute('''CREATE TABLE IF NOT EXISTS ffxiv (id BIGINT PRIMARY KEY, ffxivid BIGINT)''')
    
    @commands.command()
    async def linkff14(self, ctx, first_name:str=None, last_name:str=None, server:str=None):
        params = {'name': '{} {}'.format(first_name, last_name), 'server': server, 'private_key': conf.get("FF14_TOKEN")}
        channel = ctx.message.channel
        author_id = ctx.message.author.id
        if not first_name or not last_name or not server:
            await channel.send("Incorrect command format. Usage: `-linkff14 FIRSTNAME LASTNAME SERVER`")
            return
        try:
            r = requests.get(url="http://xivapi.com/character/search", params=params).json()
            player = r['Results'][0]
            if player['Name'].lower() != "{} {}".format(first_name, last_name).lower():
                await channel.send("Player not found, did you mean {}? Please try the command again.".format(player['Name']))
                return
            else:
                embed = discord.Embed()
                embed.set_thumbnail(url=player['Avatar'])
                embed.add_field(name="Name:", value=player['Name'], inline=False)
                embed.add_field(name="Server:", value=player['Server'].replace('\\xa0', ' '), inline=False)
                await channel.send("Your character has been linked!", embed=embed)
                with closing(self.db.cursor()) as cursor:
                    # Create `users` table if it does not exist
                    cursor.execute('INSERT INTO ffxiv (id, ffxivid) VALUES(%s, %s) ON DUPLICATE KEY UPDATE id=%s, ffxivid=%s', (author_id, player['ID'], author_id, player['ID']))
                return
                
        except Exception as e:
            print(e)
            await channel.send("Something went wrong while reaching the FFXIV servers. Please try again later.")
            return

    @commands.command()
    async def ff14profile(self, ctx, user:discord.User=None):
        if not user:
            user = ctx.message.author
        user_id = user.id
        
        channel = ctx.message.channel

        with closing(self.db.cursor()) as cursor:
            # Create `users` table if it does not exist
            cursor.execute('SELECT * FROM ffxiv WHERE id=%s', (user_id))
            response = cursor.fetchone()
            if not response:
                await channel.send("You haven't linked your FFXIV character yet. Use the `-linkff14` command to link your character, or mention another @user to view their profile.")
                return
            user_id, ff_id = response

        try:
            params = {'data': 'CJ,FC'}
            r = requests.get(url="http://xivapi.com/character/{}".format(ff_id), params=params).json()

            main_class = string.capwords(r['Character']['ActiveClassJob']['Name'].split("/")[0].strip())
            
            try:
                fc = r['FreeCompany']['Name']
            except Exception as e:
                print(e)
                fc = "-"

            embed = discord.Embed()
            embed.set_thumbnail(url=r['Character']['Avatar'])
            embed.add_field(name="Name:", value=r['Character']['Name'], inline=True)
            embed.add_field(name="Class:", value="Level {} {}".format(r['Character']['ActiveClassJob']['Level'], main_class), inline=True)
            embed.add_field(name=" ", value=" ", inline=True)
            
            embed.add_field(name="Server:", value=r['Character']['Server'], inline=True)
            embed.add_field(name="Free Company:", value=fc, inline=True)
            await channel.send(embed=embed)
            return
        except Exception as e:
            print(e)
            await channel.send("Something went wrong while reaching the FFXIV servers. Please try again later.")
            return

def setup(bot):
    bot.add_cog(FFXIV(bot))
