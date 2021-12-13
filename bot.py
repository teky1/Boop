import discord
import discord_components
import typing
from discord.ext import commands, tasks
from fun_commands.smol_fun_commands import _boop, _repeat, _say, _calc, _quote, _cat, _hello, _simp, _namemc, _upsidedown, _fancy, _wide, _kiera, _sumograss, _spoopyskin
from gaming.rps import _rps, _duelstats
from gaming.tictactoe import _tictactoe
from gaming.connectfour import _connect4
from general_commands.registeration import _registered, _register
from general_commands.bedwars_leaderboard import _bwterms, _bedwarsleaderboard, _bwscore, _graphleaderboard
from general_commands.online_cmd import _online
from general_commands.birthdays import _birthdays, _birth, _nextbirth
from general_commands.weather_cmd import _weather
from general_commands.smp_cmds import _smp
from general_commands.banner import _banner
from general_commands.mutuals import _mutuals
from general_commands.bedwars_cmds import _bwquests
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

#escape, amongus, boop testing
SAFE_SERVERS = [817412054050799626, 748241629747347556, 811439515830714378]

def dox_risk():
    async def predicate(ctx):
        return ctx.guild.id in SAFE_SERVERS
    return commands.check(predicate)

@client.event
async def on_command_error(ctx: commands.Context, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("This command is not available in this server.")
    else:
        raise error


@client.event
async def on_ready():
    discord_components.DiscordComponents(client)
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
@dox_risk()
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

@client.command(aliases=["gbwlb", "graph"])
async def graphleaderboard(ctx, equation):
    await _graphleaderboard(ctx, equation)

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
    await _hello(ctx, client)


@client.command(aliases=["ign"])
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
@dox_risk()
async def birth(ctx):
    await _birth(ctx, client)


@client.command()
async def nextbirth(ctx):
    await _nextbirth(ctx, client)

# @client.command()
# async def smp(ctx):
#    await _smp(ctx)

@client.command()
@dox_risk()
async def weather(ctx):
    await _weather(ctx)

@client.command(aliases=["ud", "flip"])
async def upsidedown(ctx):
    await _upsidedown(ctx)

@client.command()
async def fancy(ctx):
    await _fancy(ctx)

@client.command()
async def wide(ctx):
    await _wide(ctx)

@client.command()
async def banner(ctx, person: typing.Optional[discord.User]):
    target = ctx.author if person is None else person
    await _banner(ctx, target)

@client.command()
async def kiera(ctx):
    await _kiera(ctx)

@client.command(name="mutuals")
async def mutuals(ctx, person1, person2, page: typing.Optional[int] = 1):
    await _mutuals(ctx, person1, person2, page)

@mutuals.error
async def mutuals_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("**Correct Format:** !mutuals <person1> <person2>\n\nExample: !mutuals teky1 when_u")
    else:
        raise error

@client.command(aliases=["bwquest", "bwq"])
async def bwquests(ctx, ign):
    await _bwquests(ctx, ign)

@bwquests.error
async def bwquests_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("**Correct Format:** !bwquests <ign> OR !bwq <ign>")
    elif isinstance(error, commands.CommandInvokeError):
        if isinstance(error.original, json.decoder.JSONDecodeError) or isinstance(error.original, TypeError):
            await ctx.send("Could not find a player by that name.")
        else:
            raise error
    else:
        raise error

@client.command(aliases=["grass", "sg"])
async def sumograss(ctx):
    await _sumograss(ctx)

@client.command()
async def spoopyskin(ctx, name):
    await _spoopyskin(ctx, name)

@spoopyskin.error
async def spoopyskin_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("This command converts any person's skin into a spoopy skin :D"
                       "\n\n**Correct Format:** !spoopyskin <ign>")
    else:
        await ctx.send("An error occurred mbmb :P DM teky if this keeps happening")
        raise error

with open("bot_key.txt", "r") as file:
    key = file.read().split()


client.run(key[0])
