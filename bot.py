import discord
from discord.ext import commands, tasks
from fun_commands.smol_fun_commands import _boop, _repeat, _say, _calc, _quote, _cat, _hello, _simp, _namemc
from gaming.rps import _rps, _duelstats
from gaming.tictactoe import _tictactoe
from gaming.connectfour import _connect4
from general_commands.registeration import _registered, _register
from general_commands.bedwars_leaderboard import _bwterms, _bedwarsleaderboard, _bwscore
from general_commands.online_cmd import _online
from general_commands.birthdays import _birthdays, _birth, _nextbirth
from general_commands.smp_cmds import _smp
from objects.rpslist_obj import Rpsgames
from objects.tttgames_obj import TTTGames
from objects.c4games_obj import C4games
from events.reaction_event import check
from events.startup import begin
from events.message_event import do_message
import json

client = commands.Bot(command_prefix='!')

rpsgames = Rpsgames()
tttgames = TTTGames()
c4games = C4games()
with open("data/c4games.json") as in_file:
    c4games.games = json.load(in_file)


@client.event
async def on_ready():
    await begin()


@client.event
async def on_message(message):
    await do_message(message)
    await client.process_commands(message)



@client.event
async def on_raw_reaction_add(payload):
    await check(payload, rpsgames, tttgames, c4games, client)


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


@client.command(aliases=["dream"])
async def simp(ctx):
    await _simp(ctx)


@client.command(aliases=["hi"])
async def hello(ctx):
    await _hello(ctx)


@client.command()
async def namemc(ctx):
    await _namemc(ctx)

@client.command(aliases=["fl"])
async def online(ctx):
    await _online(ctx)


@client.command(aliases=["C4"])
async def c4(ctx):
    if ctx.message.content[1:3] == "c4":
        await _connect4(ctx, True, c4games, client)
    else:
        await _connect4(ctx, False, c4games, client)


@client.command()
async def birthdays(ctx):
    await _birthdays(ctx, client)


@client.command()
async def birth(ctx):
    await _birth(ctx, client)


@client.command()
async def nextbirth(ctx):
    await _nextbirth(ctx, client)

@client.command()
async def smp(ctx):
    await _smp(ctx)


with open("bot_key.txt", "r") as file:
    key = file.read().split()


client.run(key[0])
