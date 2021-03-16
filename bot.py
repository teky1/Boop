import discord
from discord.ext import commands, tasks
from fun_commands.smol_fun_commands import _boop, _repeat, _say, _calc, _quote, _cat
from gaming.samplegame import _game
from gaming.rps import _rps, _duelstats
from gaming.tictactoe import _tictactoe
from general_commands.registeration import _registered, _register
from general_commands.bedwars_leaderboard import _bwterms, _bedwarsleaderboard, _bwscore
from objects.rpslist_obj import Rpsgames
from objects.tttgames_obj import TTTGames
from events.reaction_event import check
from events.startup import begin
from events.message_event import do_message
client = commands.Bot(command_prefix='!')

rpsgames = Rpsgames()
tttgames = TTTGames()

@client.event
async def on_ready():
    await begin()


@client.event
async def on_message(message):
    await do_message(message)
    await client.process_commands(message)



@client.event
async def on_raw_reaction_add(payload):
    await check(payload, rpsgames, tttgames)


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
async def quote(ctx):
    await _quote(ctx)

@client.command()
async def cat(ctx):
    await _cat(ctx)

@client.command()
async def rps(ctx):
    await _rps(ctx, client, rpsgames)


@client.command()
async def rpsstats(ctx):
    await _duelstats(ctx, client)

@client.command(aliases=["ttt"])
async def tictactoe(ctx):
    await _tictactoe(ctx, client, tttgames)

with open("bot_key.txt", "r") as file:
    key = file.read().split()


client.run(key[0])
