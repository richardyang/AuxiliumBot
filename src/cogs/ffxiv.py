import pymysql
import discord
import requests
import string
import math
import traceback

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
            track = traceback.format_exc()
            print(track)
            await channel.send("Something went wrong while reaching the FFXIV servers. Please try again later.")
            return

    @commands.command()
    async def ff14profile(self, ctx, user:discord.User=None):
        if not user:
            user = ctx.message.author
        user_id = user.id
        
        channel = ctx.message.channel

        with closing(self.db.cursor()) as cursor:
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
            player_levels = {c['Name'].replace(" ", "").split("/")[-1]:c['Level'] for c in r['Character']['ClassJobs']}

            try:
                fc = r['FreeCompany']['Name']
            except Exception as e:
                print(e)
                fc = "-"

            embed = discord.Embed()
            embed.set_thumbnail(url=r['Character']['Avatar'])
            embed.add_field(name="Name:", value=r['Character']['Name'], inline=True)
            embed.add_field(name="Server:", value=r['Character']['Server'], inline=True)
            embed.add_field(name="\u200B", value="\u200B", inline=True)
            
            embed.add_field(name="Active Job:", value="Level {} {}".format(r['Character']['ActiveClassJob']['Level'], main_class), inline=True)
            embed.add_field(name="Free Company:", value=fc, inline=True)
            embed.add_field(name="\u200B", value="\u200B", inline=True)

            n = math.ceil(len(player_levels)/3)
            partitions = [list(player_levels.keys())[i:i + n] for i in range(0, len(player_levels), n)]
            assert len(partitions) == 3
            for classes in partitions:
                class_list_str = ""
                for c in classes:
                    class_list_str += "{}: {} \n".format(conf["FFXIV_CLASS_ICONS"][c], player_levels[c])
                embed.add_field(name="\u200B", value=class_list_str, inline=True)

            await channel.send(embed=embed)
            return
        except Exception as e:
            track = traceback.format_exc()
            print(track)
            await channel.send("Something went wrong while reaching the FFXIV servers. Please try again later.")
            return

    @commands.command()
    async def ff14gear(self, ctx, user:discord.User=None):
        if not user:
            user = ctx.message.author
        user_id = user.id
        
        channel = ctx.message.channel

        with closing(self.db.cursor()) as cursor:
            cursor.execute('SELECT * FROM ffxiv WHERE id=%s', (user_id))
            response = cursor.fetchone()
            if not response:
                await channel.send("You haven't linked your FFXIV character yet. Use the `-linkff14` command to link your character, or mention another @user to view their profile.")
                return
            user_id, ff_id = response

        try:
            params = {'extended': '1', 'data':'CJ'}
            r = requests.get(url="http://xivapi.com/character/{}".format(ff_id), params=params).json()
            
            main_class = string.capwords(r['Character']['ActiveClassJob']['Name'].split("/")[0].strip())
            
            gear_dict = {
                "MainHand": '-',
                "Head": '-',
                "Body": '-',
                "Hands": '-',
                "Waist": '-',
                "Legs": '-',
                "Feet": '-',
                "OffHand": '-',
                "Earrings": '-',
                "Necklace": '-',
                "Bracelets": '-',
                "Ring1": '-',
                "Ring2": '-',
                "SoulCrystal": '-'
            }

            for slot, item in r['Character']['GearSet']['Gear'].items():
                gear_dict[slot] = "{} [{}]".format(item['Item']['Name'], item['Item']['LevelItem'])

            embed = discord.Embed()
            embed.set_thumbnail(url=r['Character']['Avatar'])
            embed.add_field(name="Name:", value=r['Character']['Name'], inline=True)
            embed.add_field(name="Active Job:", value="Level {} {}".format(r['Character']['ActiveClassJob']['Level'], main_class), inline=True)
            embed.add_field(name="\u200B", value="\u200B", inline=True)

            n = math.ceil(len(gear_dict)/2)
            partitions = [list(gear_dict.keys())[i:i + n] for i in range(0, len(gear_dict), n)]
            assert len(partitions) == 2
            for i in range(len(partitions[0])):
                embed.add_field(name="**{}**".format(partitions[0][i]), value=gear_dict[partitions[0][i]], inline=True)
                embed.add_field(name="**{}**".format(partitions[1][i]), value=gear_dict[partitions[1][i]], inline=True)
                embed.add_field(name="\u200B", value='\u200B', inline=True)

            await channel.send(embed=embed)
            return
        except Exception as e:
            track = traceback.format_exc()
            print(track)
            await channel.send("Something went wrong while reaching the FFXIV servers. Please try again later.")
            return

    @commands.command()
    async def ff14search(self, ctx, *args):
        search_string = " ".join(args)
        channel = ctx.message.channel

        server = None
        with closing(self.db.cursor()) as cursor:
            cursor.execute('SELECT * FROM ffxiv WHERE id=%s', (ctx.message.author.id))
            response = cursor.fetchone()
        
        try:
            if response:
                _, ff_id = response
                server = requests.get(url="http://xivapi.com/character/{}".format(ff_id)).json()['Character']['Server']

            params = {'indexes': 'Item', 'string_algo': 'fuzzy', 'string': search_string}
            r = requests.get(url="http://xivapi.com/search", params=params).json()
            if len(r['Results']) == 0:
                await channel.send("Did not find any items matching your search.")
                return
            
            item_id = r['Results'][0]['ID']
            item = requests.get(url="https://xivapi.com/item/{}".format(item_id)).json()
            
            embed = discord.Embed(
                title=item['Name'], 
                description="{}\n{}".format(item['ItemSearchCategory']['Name'], item['Description']), 
                url="https://www.garlandtools.org/db/#item/{}".format(item_id))
            embed.set_thumbnail(url="https://www.garlandtools.org/files/icons/item/{}.png".format(item["IconID"]))
            
            await channel.send(embed=embed)
            return    

        except Exception as e:
            print(e)
            await channel.send("Something went wrong while reaching the FFXIV servers. Please try again later.")
            return





def setup(bot):
    bot.add_cog(FFXIV(bot))
