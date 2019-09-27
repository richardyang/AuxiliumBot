import config

import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='-')

@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')

@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Yuki's Morale"))
    
bot.load_extension(f'cogs.levels')
bot.load_extension(f'cogs.fun')
bot.load_extension(f'cogs.rater')
bot.load_extension(f'cogs.gamble')
bot.load_extension(f'cogs.tracker')
bot.run(config.TOKEN)
