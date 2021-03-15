import discord
from discord.ext import commands, tasks
from fun_commands.smol_fun_commands import _boop, _repeat, _say, _calc
from gaming.samplegame import _game
from gaming.rps import _rps, rpsgame, _duelstats
from general_commands.registeration import _registered, _register
from general_commands.bedwars_leaderboard import _bwterms, _bedwarsleaderboard, _bwscore
from time import strftime, localtime

client = commands.Bot(command_prefix='!')

games = []


@client.event
async def on_ready():
    print(f"bot started {strftime('%I:%M %p, %m/%d', localtime())}")  # use %c for a full, pre-made date


@client.event
async def on_raw_reaction_add(payload):
    if not payload.user_id == 811435588942692352:
        for game in games:
            await rpsgame(payload, game)


@client.command()
async def boop(ctx, who: discord.User):
    await _boop(ctx, who)


@client.command()
async def repeat(ctx):
    await _repeat(ctx)


@client.command()
async def say(ctx):
    await _say(ctx)


@client.command()
async def calc(ctx):
    await _calc(ctx)


@client.command()
async def game(ctx):
    await _game(ctx, "Cool Game", client)


@client.command()
async def registered(ctx):
    await _registered(ctx)


@client.command()
async def register(ctx, ign):
    await _register(ctx, ign)


@client.command()
async def bwterms(ctx):
    await _bwterms(ctx)


@client.command()
async def bwscore(ctx, ign, equation):
    await _bwscore(ctx, ign, equation)


@client.command(aliases=["bwlb"])
async def bwleaderboard(ctx, equation):
    await _bedwarsleaderboard(ctx, equation)


@client.command()
async def rps(ctx):
    thisgame = await _rps(ctx, client)
    games.append(thisgame)


@client.command()
async def duelstats(ctx):
    await _duelstats(ctx, client)


with open("bot_key.txt", "r") as file:
    key = file.read().split()


client.run(key[0])
