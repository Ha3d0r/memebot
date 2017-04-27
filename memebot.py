import discord
import aiohttp
from discord.ext import commands
from wn8 import *
from classify import *
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
    
    async with aiohttp.get("https://wot-life.com/eu/player/" + user + "/") as request:
        if request.status == 200:
            classification = PlayerClassification(BeautifulSoup(await request.text(), "html.parser"))
            
            await bot.say(classification.report())
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

    r_type = RecentType.OVERALL

    if period == "24h":
        r_type = RecentType.DAY
    elif period == "7d":
        r_type = RecentType.WEEK
    elif period == "30d":
        r_type = RecentType.MONTH
    elif period == "":
        r_type == RecentType.OVERALL
    else:
        await bot.say("Invalid period supplied")
        return
    
    async with aiohttp.get("https://wot-life.com/eu/player/" + user + "/") as request:
        if request.status == 200:
            stats = read_stats(await request.text())
            
            await bot.say(stats.readable_stats(r_type))
        else:
            await bot.say("Invalid request")

# fetch the token
token_file = open("token")
token = token_file.read()

print(token)

bot.run(token)