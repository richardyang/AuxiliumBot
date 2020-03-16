import os
import random
import discord
import time
import pymysql
import json
import numpy as np

from config import conf
from contextlib import closing
from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.src_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))
        self.db = self.bot.get_cog('Database').db

        with closing(self.db.cursor()) as cursor:
            cursor = self.db.cursor()
            # Create `users` table if it does not exist
            cursor.execute('''CREATE TABLE IF NOT EXISTS battle (user_id INTEGER PRIMARY KEY, class VARCHAR(5000), wins INTEGER, losses INTEGER, pvp INTEGER)''')
        
        with open(os.path.join(self.src_dir, "cogs/battle_classes.json"), "r") as fp:
            self.battle_classes = json.load(fp)
        self.running_battles = 0
        self.economy_cog = self.bot.get_cog("Economy")

    @commands.Cog.listener()
    async def on_message(self, message):
        # Do nothing if author is self
        if message.author == self.bot.user:
            return
        # Do nothing if author is bot
        if message.author.bot:
            return
        
        if "can i get an f" in message.content.lower() or "can i get a f" in message.content.lower():
            await message.add_reaction(emoji="🇫")
        return

    @commands.command(name='8ball')
    async def eightball(self, ctx):
        """
        -8ball <question> -> ask 8ball a question and see the response
        """
        channel = ctx.message.channel
        if ctx.message.content.strip() == "-8ball":
            img = discord.File(os.path.join(self.src_dir,'img/8ball_0.png'))
            await channel.send("Type a question after the command!", file=img)
        else:
            r = random.randint(1,5)
            img = discord.File(os.path.join(self.src_dir,'img/8ball_{}.png'.format(r)))
            await channel.send(file=img)

    @commands.command(name='listclasses')
    async def listclasses(self, ctx):
        """
        -listclasses -> list all the available classes for pvp function
        """
        channel = ctx.message.channel
        await channel.send("Available classes: `{}` \n Use -setclass <classname> to set your class.".format(', '.join(list(self.battle_classes.keys()))))

    @commands.command()
    async def setclass(self, ctx, class_str):
        """
        -setclass <class> -> changes player pvp class, use -listclasses to see all classes
        """
        if class_str not in self.battle_classes.keys():
            await ctx.channel.send("{} is not a valid class option, choose from: `{}`".format(class_str, ', '.join(list(self.battle_classes.keys()))))
            return
        with closing(self.db.cursor()) as cursor:
            cursor.execute('SELECT * FROM battle WHERE user_id=%s', (str(ctx.author.id),) )
            query_response = cursor.fetchone()

        if not query_response:
            # Add new user to table if they do not exist
            query_response = (str(ctx.author.id), class_str, 0, 0, 0)
            with closing(self.db.cursor()) as cursor:
                cursor.execute('INSERT INTO battle VALUES (%s,%s,%s,%s,%s)', query_response)
                self.db.commit()
        else:
            # User exists, update their class
            user_id, old_class_str, wins, losses, pvp = query_response
            with closing(self.db.cursor()) as cursor:
                cursor.execute('UPDATE battle SET class=%s, wins=%s, losses=%s, pvp=%s WHERE user_id=%s', (class_str, wins, losses, pvp, user_id))
                self.db.commit()
        await ctx.channel.send("Your battle class has been set to {}".format(self.battle_classes[class_str]["name"]))
        return

    @commands.command()
    async def enablepvp(self, ctx):
        """
        -enablepvp -> enables pvp mode, allows battles for coin wagers
        """
        with closing(self.db.cursor()) as cursor:
            cursor.execute('SELECT * FROM battle WHERE user_id=%s', (str(ctx.author.id),) )
            query_response = cursor.fetchone()

        if not query_response:
            # Add new user to table if they do not exist
            await ctx.channel.send("You did not select a class. A random one has been assigned to you. Use the `-setclass` command to change your class.")
            class_str = random.choice(list(self.battle_classes.keys()))
            query_response = (str(ctx.author.id), class_str, 0, 0, 1)
            with closing(self.db.cursor()) as cursor:
                cursor.execute('INSERT INTO battle VALUES (%s,%s,%s,%s,%s)', query_response)
                self.db.commit()
        else:
            # User exists, update their class
            user_id, class_str, wins, losses, pvp = query_response
            with closing(self.db.cursor()) as cursor:
                cursor.execute('UPDATE battle SET class=%s, wins=%s, losses=%s, pvp=%s WHERE user_id=%s', (class_str, wins, losses, 1, user_id))
                self.db.commit()
        await ctx.channel.send("Warning: you have enabled PvP mode. Anyone can attack you now with the `-pvp` command, and you may win/lose coins from PvP battles. Use the `-disablepvp` command to disable PvP mode.")
        return

    @commands.command()
    async def disablepvp(self, ctx):
        """
        -disablepvp -> disables pvp mode, battles can be fought but no wagers
        """
        with closing(self.db.cursor()) as cursor:
            cursor.execute('SELECT * FROM battle WHERE user_id=%s', (str(ctx.author.id),) )
            query_response = cursor.fetchone()

        if not query_response:
            # Add new user to table if they do not exist
            await ctx.channel.send("You did not select a class. A random one has been assigned to you. Use the `-setclass` command to change your class.")
            class_str = random.choice(list(self.battle_classes.keys()))
            query_response = (str(ctx.author.id), class_str, 0, 0, 0)
            with closing(self.db.cursor()) as cursor:
                cursor.execute('INSERT INTO battle VALUES (%s,%s,%s,%s,%s)', query_response)
                self.db.commit()
        else:
            # User exists, update their class
            user_id, class_str, wins, losses, pvp = query_response
            with closing(self.db.cursor()) as cursor:
                cursor.execute('UPDATE battle SET class=%s, wins=%s, losses=%s, pvp=%s WHERE user_id=%s', (class_str, wins, losses, 0, user_id))
                self.db.commit()
        await ctx.channel.send("You have disabled PvP mode.")
        return

    @commands.command()
    async def pvp(self, ctx, user1:discord.User, wager:int):
        """
        -pvp <@user> <wager> -> challenges user to battle with a wager, winner takes all
        """
        if self.running_battles > 5:
            await ctx.channel.send("There are too many battles going on. Wait a bit before initiating another one.")
            return

        initiator = ctx.message.author
        target = user1
        initiator_hp = 100
        target_hp = 100

        # Get initiator class
        with closing(self.db.cursor()) as cursor:
            cursor.execute('SELECT * FROM battle WHERE user_id=%s', (str(initiator.id),) )
            query_response = cursor.fetchone()
        if not query_response or not query_response[4]:
            await ctx.channel.send("You do not have PvP mode enabled. Type `-enablepvp` or use `-battle` to fight without betting.")
            return
        else:
            initiator_class = query_response[1]
            initiator_icon = self.battle_classes[initiator_class]["name"]
            initiator_attacks = self.battle_classes[initiator_class]["attacks"]
            initiator_blocks = self.battle_classes[initiator_class]["blocks"]
            initiator_heals = self.battle_classes[initiator_class]["heals"]

        # Get target class
        with closing(self.db.cursor()) as cursor:
            cursor.execute('SELECT * FROM battle WHERE user_id=%s', (str(target.id),) )
            query_response = cursor.fetchone()
        if not query_response or not query_response[4]:
            await ctx.channel.send("Your opponent does not have PvP mode enabled. Use `-battle` to fight without betting.")
            return
        else:
            target_class = query_response[1]
            target_icon = self.battle_classes[target_class]["name"]
            target_attacks = self.battle_classes[target_class]["attacks"]
            target_blocks = self.battle_classes[target_class]["blocks"]
            target_heals = self.battle_classes[target_class]["heals"]

        wager = abs(wager)
        # Check if initiator has enough coins to place the wager
        iid, ilvl, iexp, ipoints = self.economy_cog.get_global_user_data(initiator.id)
        if wager > ipoints:
            await ctx.channel.send("You don't have enough coins to initiate this battle. Your current balance is {}.".format(ipoints))
            return
        # Check if wager is not > 10% of the target's coins
        tid, tlvl, texp, tpoints = self.economy_cog.get_global_user_data(target.id)
        if wager > int(0.1 * tpoints):
            await ctx.channel.send("You cannot wager more than 10 percent of your opponent's current balance. Their current balance is {}, and the max wager is {}.".format(tpoints, int(0.1*tpoints)))
            return
        
        self.running_battles += 1
        
        log = "💀 PvP Battle: {} vs {} 💀\n".format(initiator.name, target.name)
        embed = discord.Embed(description=log, color=0x008000)
        embed.add_field(name=initiator.name, value="100/100", inline=True)
        embed.add_field(name=target.name, value="100/100", inline=True)
        msg = await ctx.channel.send(embed=embed)

        initiatorTurn = True
        while initiator_hp > 0 and target_hp > 0:
            if initiatorTurn:
                action = np.random.choice(["attacks", "blocks", "heals"], p=[0.8, 0.1, 0.1])
                if action == "attacks":
                    dmg = random.randint(10,30)
                    skill = random.choice(initiator_attacks)
                    target_hp = max(0, target_hp-dmg)
                    dmg_str = "__**{}**__ hit __**{}**__ for **{}** dmg using {}".format(initiator.name, target.name, dmg, skill)
                elif action == "blocks":
                    skill = random.choice(target_blocks)
                    dmg_str = "__**{}**__ blocked __**{}**__'s attack using {}".format(target.name, initiator.name, skill)
                elif action == "heals":
                    dmg = random.randint(10,30)
                    skill = random.choice(initiator_heals)
                    initiator_hp = min(100, initiator_hp+dmg)
                    dmg_str = "__**{}**__ healed for **{}** dmg using {}".format(initiator.name, dmg, skill)
                embed = discord.Embed(description="{} {}".format(log, dmg_str), color=0x008000)
                embed.add_field(name=initiator.name + " " + initiator_icon, value="{}/100".format(initiator_hp), inline=True)
                embed.add_field(name=target.name + " " + target_icon, value="{}/100".format(target_hp), inline=True)
                log += dmg_str + "\n"
            else:
                action = np.random.choice(["attacks", "blocks", "heals"], p=[0.8, 0.1, 0.1])
                if action == "attacks":
                    dmg = random.randint(10,30)
                    skill = random.choice(target_attacks)
                    initiator_hp = max(0, initiator_hp-dmg)
                    dmg_str = "__**{}**__ hit __**{}**__ for **{}** dmg using {}".format(target.name, initiator.name, dmg, skill)
                elif action == "blocks":
                    skill = random.choice(initiator_blocks)
                    dmg_str = "__**{}**__ blocked __**{}**__'s attack using {}".format(initiator.name, target.name, skill)
                elif action == "heals":
                    dmg = random.randint(10,30)
                    skill = random.choice(target_heals)
                    target_hp = min(100, target_hp+dmg)
                    dmg_str = "__**{}**__ healed for **{}** dmg using {}".format(target.name, dmg, skill)
                embed = discord.Embed(description="{} {}".format(log, dmg_str), color=0xff0000)
                embed.add_field(name=initiator.name + " " + initiator_icon, value="{}/100".format(initiator_hp), inline=True)
                embed.add_field(name=target.name + " " + target_icon, value="{}/100".format(target_hp), inline=True)
                log += dmg_str + "\n"
            
            await msg.edit(embed=embed)
            initiatorTurn = not(initiatorTurn)
            time.sleep(1.5)
        
        if initiator_hp == 0:
            embed = discord.Embed(description="{} \n 🏆 __**{}**__ has won the battle and {} coins!".format(log, target.name, wager), color=0xff0000)
            embed.add_field(name=initiator.name + " " + initiator_icon, value="{}/100".format(initiator_hp), inline=True)
            embed.add_field(name=target.name + " " + target_icon, value="{}/100".format(target_hp), inline=True)
            await self.economy_cog.set_global_user_data(tid, tlvl, texp, tpoints+wager)
            await self.economy_cog.set_global_user_data(iid, ilvl, iexp, ipoints-wager)

        else:
            embed = discord.Embed(description="{} \n 🏆 __**{}**__ has won the battle and {} coins!".format(log, initiator.name, wager), color=0x008000)
            embed.add_field(name=initiator.name + " " + initiator_icon, value="{}/100".format(initiator_hp), inline=True)
            embed.add_field(name=target.name + " " + target_icon, value="{}/100".format(target_hp), inline=True)
            await self.economy_cog.set_global_user_data(tid, tlvl, texp, tpoints-wager)
            await self.economy_cog.set_global_user_data(iid, ilvl, iexp, ipoints+wager)

        await msg.edit(embed=embed)
        self.running_battles -= 1
        return 


    @commands.command()
    async def battle(self, ctx, user1:discord.User=None, user2:discord.User=None):
        """
        -pvp <@user> -> challenges a user to battle for fun, no wagers involved
        """
        if self.running_battles > 5:
            await ctx.channel.send("There are too many battles going on. Wait a bit before initiating another one.")
            return
        self.running_battles += 1

        if not user2:
            initiator = ctx.message.author
            target = user1
        else:
            initiator = user1
            target = user2
        
        initiator_hp = 100
        target_hp = 100

        # Get initiator class
        with closing(self.db.cursor()) as cursor:
            cursor.execute('SELECT * FROM battle WHERE user_id=%s', (str(initiator.id),) )
            query_response = cursor.fetchone()
        if not query_response:
            initiator_class = random.choice(list(self.battle_classes.keys()))
        else:
            initiator_class = query_response[1]
        initiator_icon = self.battle_classes[initiator_class]["name"]
        initiator_attacks = self.battle_classes[initiator_class]["attacks"]
        initiator_blocks = self.battle_classes[initiator_class]["blocks"]
        initiator_heals = self.battle_classes[initiator_class]["heals"]

        # Get target class
        with closing(self.db.cursor()) as cursor:
            cursor.execute('SELECT * FROM battle WHERE user_id=%s', (str(target.id),) )
            query_response = cursor.fetchone()
        if not query_response:
            target_class = random.choice(list(self.battle_classes.keys()))
        else:
            target_class = query_response[1]
        target_icon = self.battle_classes[target_class]["name"]
        target_attacks = self.battle_classes[target_class]["attacks"]
        target_blocks = self.battle_classes[target_class]["blocks"]
        target_heals = self.battle_classes[target_class]["heals"]

        # Calculating probability distribution of each player's actions
        initiator_actions_total = len(initiator_attacks) + len(initiator_heals) + len(target_blocks) # target blocks is intentional
        # initiator_probs = [action/initiator_actions_total for action in [len(initiator_attacks), len(target_blocks), len(initiator_heals)]]
        initiator_probs = [0.8, 0.1, 0.1]

        target_actions_total = len(target_attacks) + len(target_heals) + len(initiator_blocks) # initiator blocks is intentional
        # target_probs = [action/target_actions_total for action in [len(target_attacks), len(initiator_blocks), len(target_heals)]]
        target_probs = [0.8, 0.1, 0.1]

        embed = discord.Embed(description="Arena Battle: {} vs {}".format(initiator.name, target.name), color=0x008000)
        embed.add_field(name=initiator.name, value="100/100", inline=True)
        embed.add_field(name=target.name, value="100/100", inline=True)
        msg = await ctx.channel.send(embed=embed)

        initiatorTurn = True
        log = ""
        while initiator_hp > 0 and target_hp > 0:
            if initiatorTurn:
                action = np.random.choice(["attacks", "blocks", "heals"], p=initiator_probs)
                if action == "attacks":
                    dmg = random.randint(10,40)
                    skill = random.choice(initiator_attacks)
                    target_hp = max(0, target_hp-dmg)
                    dmg_str = "__**{}**__ hit __**{}**__ for **{}** dmg using {}".format(initiator.name, target.name, dmg, skill)
                elif action == "blocks":
                    skill = random.choice(target_blocks)
                    dmg_str = "__**{}**__ blocked __**{}**__'s attack using {}".format(target.name, initiator.name, skill)
                elif action == "heals":
                    dmg = random.randint(10,40)
                    skill = random.choice(initiator_heals)
                    initiator_hp = min(100, initiator_hp+dmg)
                    dmg_str = "__**{}**__ healed for **{}** dmg using {}".format(initiator.name, dmg, skill)
                embed = discord.Embed(description="{} {}".format(log, dmg_str), color=0x008000)
                embed.add_field(name=initiator.name + " " + initiator_icon, value="{}/100".format(initiator_hp), inline=True)
                embed.add_field(name=target.name + " " + target_icon, value="{}/100".format(target_hp), inline=True)
                log += dmg_str + "\n"
            else:
                action = np.random.choice(["attacks", "blocks", "heals"], p=target_probs)
                if action == "attacks":
                    dmg = random.randint(10,40)
                    skill = random.choice(target_attacks)
                    initiator_hp = max(0, initiator_hp-dmg)
                    dmg_str = "__**{}**__ hit __**{}**__ for **{}** dmg using {}".format(target.name, initiator.name, dmg, skill)
                elif action == "blocks":
                    skill = random.choice(initiator_blocks)
                    dmg_str = "__**{}**__ blocked __**{}**__'s attack using {}".format(initiator.name, target.name, skill)
                elif action == "heals":
                    dmg = random.randint(10,40)
                    skill = random.choice(target_heals)
                    target_hp = min(100, target_hp+dmg)
                    dmg_str = "__**{}**__ healed for **{}** dmg using {}".format(target.name, dmg, skill)
                embed = discord.Embed(description="{} {}".format(log, dmg_str), color=0xff0000)
                embed.add_field(name=initiator.name + " " + initiator_icon, value="{}/100".format(initiator_hp), inline=True)
                embed.add_field(name=target.name + " " + target_icon, value="{}/100".format(target_hp), inline=True)
                log += dmg_str + "\n"
            
            await msg.edit(embed=embed)
            initiatorTurn = not(initiatorTurn)
            time.sleep(1.5)
        
        if initiator_hp == 0:
            embed = discord.Embed(description="{} \n 🏆 __**{}**__ has won the battle!".format(log, target.name), color=0xff0000)
            embed.add_field(name=initiator.name + " " + initiator_icon, value="{}/100".format(initiator_hp), inline=True)
            embed.add_field(name=target.name + " " + target_icon, value="{}/100".format(target_hp), inline=True)
        else:
            embed = discord.Embed(description="{} \n 🏆 __**{}**__ has won the battle!".format(log, initiator.name), color=0x008000)
            embed.add_field(name=initiator.name + " " + initiator_icon, value="{}/100".format(initiator_hp), inline=True)
            embed.add_field(name=target.name + " " + target_icon, value="{}/100".format(target_hp), inline=True)
        
        await msg.edit(embed=embed)
        self.running_battles -= 1
        return            


def setup(bot):
    bot.add_cog(Fun(bot))