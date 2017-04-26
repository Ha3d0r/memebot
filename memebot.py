import discord
from discord.ext import commands
import random
import wn8
from wn8 import fetch_wn8

description = '''An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here.'''
bot = commands.Bot(command_prefix='.', description=description)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def wn8(user):
    """Fetches the wn8 of a particular user"""
    
    await bot.say(fetch_wn8(user))

# fetch the token
token_file = open("token")
token = token_file.read()

print(token)

bot.run(token)