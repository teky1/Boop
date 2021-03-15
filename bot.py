import discord
from discord.ext import commands, tasks
from fun_commands.smol_fun_commands import _boop, _repeat, _say, _calc
from time import strftime, localtime


client = commands.Bot(command_prefix='!')


@client.event
async def on_ready():
    print(f"bot started {strftime('%I:%M %p, %m/%d', localtime())}")  # use %c for a full, pre-made date


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

with open("bot_key.txt", "r") as file:
    key = file.read().split()


client.run(key[0])
