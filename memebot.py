import discord
import aiohttp
import hashlib
from discord.ext import commands
from commands.wn8 import *
from commands.classify import classify_player
from bs4 import BeautifulSoup
from random import choice

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

@bot.command()
async def rate(*, subject):
    """Rates something or someone"""

    lowered = subject.lower()

    # hash the lowercase input to an int
    hash_object = hashlib.sha1(lowered.encode())
    hash_number = int(hash_object.hexdigest(), 16)

    mod = hash_number % 11

    if lowered in ["memebot", "me", "apptux"]:
        mod = 10

    reaction = ""

    if 0 <= mod <= 3:
        reaction = ":weary:"
    elif 4 <= mod <= 6:
        reaction = ":confused:"
    elif 7 <= mod <= 9:
        reaction = ":grin:"
    else:
        reaction = ":heart_eyes:"
    
    await bot.say(f":thinking: I rate {subject} {mod}/10 " + reaction)

@bot.command()
async def choose(*, input: str):
    options = list(map(lambda x: x.strip(), input.split(',')))
    
    if len(options) == 0:
        await bot.say(":fearful: Please supply a list of comma separated options")
        return
    
    await bot.say(":thinking: I choose: " + choice(options))

# fetch the token
token_file = open("token")
token = token_file.read()

print(token)

bot.run(token)