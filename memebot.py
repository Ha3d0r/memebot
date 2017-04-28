import discord
import aiohttp
from discord.ext import commands
from wn8 import *
from classify import classify_player
from bs4 import BeautifulSoup

description = '''Just memes'''
bot = commands.Bot(command_prefix='.', description=description)

@bot.event
async def on_ready():
    await bot.change_presence(game=discord.Game(name='with urmum'))
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def classify(user = ""):
    """Classifies a WoT user"""

    if user == "":
        await bot.say("No username entered")
        return

    if user.lower() == "memebot":
        await bot.say(":heart_eyes: best bot ever :heart_eyes:")
        return
    
    async with aiohttp.get("https://wot-life.com/eu/player/" + user + "/") as request:
        if request.status == 200:
            await bot.say(classify_player(await request.text(), user))
        else:
            await bot.say("Invalid request")

@bot.command()
async def wn8(user = "", period = ""):
    """Fetches the wn8 of <user>.
    user: username in WoT
    period: 24h/7d/30d, leave empty for overall wn8
    """

    if user == "":
        await bot.say("No username entered")
        return
    
    async with aiohttp.get("https://wot-life.com/eu/player/" + user + "/") as request:
        if request.status == 200:            
            await bot.say(read_stats(await request.text(), period))
        else:
            await bot.say("Invalid request")

# fetch the token
token_file = open("token")
token = token_file.read()

print(token)

bot.run(token)