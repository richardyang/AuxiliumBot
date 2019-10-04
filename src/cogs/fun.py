import os
import random
import discord
import time
from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.src_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))

        self.icons = {'guardian': '<:guardian:629574093758267413>','warrior': '<:warrior:629574093947142144>'}
        self.skills = {'guardian': ["Virtue of Justice",
                                    "Vengeful Strike",
                                    "Wrathful Strike",
                                    "Whirling Wrath",
                                    "Leap of Faith",
                                    "Symbol of Wrath",
                                    "Binding Blade",
                                    "Hammer Bash",
                                    "Mighty Blow",
                                    "Zealot's Embrace",
                                    "Banish",
                                    "Wave of Wrath",
                                    "Holy Strike",
                                    "Symbol of Faith",
                                    "Orb of Wrath",
                                    "Symbol of Punishment",
                                    "Chains of Light",
                                    "Sword of Wrath",
                                    "Ray of Judgment",
                                    "Shield of Judgment",
                                    "Zealot's Flame",
                                    "Cleansing Flame",
                                    "Hallowed Ground",
                                    "Purging Flames",
                                    "Judge's Intervention",
                                    "Smite Condition",
                                    "Bane Signet",
                                    "True Shot",
                                    "Dragon's Maw",
                                    "Procession of Blades"],
                        'warrior':["Hundred Blades",
                                    "Whirlwind Attack",
                                    "Bladetrail",
                                    "Rush",
                                    "Earthshaker",
                                    "Hammer Bash",
                                    "Fierce Blow",
                                    "Staggering Blow",
                                    "Backbreaker",
                                    "Fan of Fire",
                                    "Arcing Arrow",
                                    "Eviscerate",
                                    "Cyclone Axe",
                                    "Whirling Axe",
                                    "Flurry",
                                    "Sever Artery",
                                    "Savage Leap",
                                    "Shield Bash"]
                    }

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
        channel = ctx.message.channel
        if ctx.message.content.strip() == "-8ball":
            img = discord.File(os.path.join(self.src_dir,'img/8ball_0.png'))
            await channel.send("Type a question after the command!", file=img)
        else:
            r = random.randint(1,5)
            img = discord.File(os.path.join(self.src_dir,'img/8ball_{}.png'.format(r)))
            await channel.send(file=img)
    
    @commands.command()
    async def billy(self, ctx):
        print("Press F for Billy")
        channel = ctx.message.channel
        file = discord.File(os.path.join(self.src_dir, 'img/billy.gif'))
        msg = await channel.send("Press F to pay respects", file=file)
        await msg.add_reaction(emoji="🇫")

    @commands.command()
    async def battle(self, ctx, user1:discord.User=None, user2:discord.User=None):
        if not user2:
            initiator = ctx.message.author
            target = user1
        else:
            initiator = user1
            target = user2
        
        initiator_hp = 100
        target_hp = 100

        initiator_class = random.choice(list(self.skills.keys()))
        target_class = random.choice(list(self.skills.keys()))

        embed = discord.Embed(description="DEATHBATTLE: {} vs {}".format(initiator.name, target.name), color=0x008000)
        embed.add_field(name=initiator.name, value="100/100", inline=True)
        embed.add_field(name=target.name, value="100/100", inline=True)
        msg = await ctx.channel.send(embed=embed)

        initiatorTurn = True
        last_str = ""
        while initiator_hp > 0 and target_hp > 0:
            dmg = random.randint(0,20)
            if initiatorTurn:
                target_hp = max(0, target_hp-dmg)
                if dmg:
                    skill = random.choice(self.skills[initiator_class])
                    dmg_str = "__**{}**__ hit __**{}**__ for **{}** dmg using {}".format(initiator.name, target.name, dmg, skill)
                else:
                    dmg_str = "__**{}**__ blocked __**{}**__'s attack!".format(target.name, initiator.name)
                embed = discord.Embed(description="{} \n {}".format(last_str, dmg_str), color=0x008000)
                embed.add_field(name=initiator.name + " " + self.icons[initiator_class], value="{}/100".format(initiator_hp), inline=True)
                embed.add_field(name=target.name + " " + self.icons[target_class], value="{}/100".format(target_hp), inline=True)
                last_str = dmg_str
            else:
                initiator_hp = max(0, initiator_hp-dmg)
                if dmg:
                    skill = random.choice(self.skills[target_class])
                    dmg_str = "__**{}**__ hit __**{}**__ for **{}** dmg using {}".format(target.name, initiator.name, dmg, skill)
                else:
                    dmg_str = "__**{}**__ blocked __**{}**__'s attack!".format(initiator.name, target.name)
                embed = discord.Embed(description="{} \n {}".format(last_str, dmg_str), color=0xff0000)
                embed.add_field(name=initiator.name + " " + self.icons[initiator_class], value="{}/100".format(initiator_hp), inline=True)
                embed.add_field(name=target.name + " " + self.icons[target_class], value="{}/100".format(target_hp), inline=True)
                last_str = dmg_str
            
            await msg.edit(embed=embed)
            initiatorTurn = not(initiatorTurn)
            time.sleep(1.5)
        
        if initiator_hp == 0:
            embed = discord.Embed(description="{} \n 🏆 __**{}**__ has won the battle!".format(last_str, target.name), color=0xff0000)
            embed.add_field(name=initiator.name + " " + self.icons[initiator_class], value="{}/100".format(initiator_hp), inline=True)
            embed.add_field(name=target.name + " " + self.icons[target_class], value="{}/100".format(target_hp), inline=True)
        else:
            embed = discord.Embed(description="{} \n 🏆 __**{}**__ has won the battle!".format(last_str, initiator.name), color=0x008000)
            embed.add_field(name=initiator.name + " " + self.icons[initiator_class], value="{}/100".format(initiator_hp), inline=True)
            embed.add_field(name=target.name + " " + self.icons[target_class], value="{}/100".format(target_hp), inline=True)
        
        await msg.edit(embed=embed)
        return            


def setup(bot):
    bot.add_cog(Fun(bot))