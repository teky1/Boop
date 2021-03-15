import discord
from discord.ext import commands, tasks
from fun_commands.smol_fun_commands import _boop

client = commands.Bot(command_prefix='!')

@client.command()
async def boop(ctx, who: discord.User):
    await _boop(ctx, who)


print("booooooooooooooooooooooooooooooooooooooooob")

print("thjis isnf bransf change")

with open("bot_key.txt", "r") as file:
    key = file.read().split()

client.run(key[0])
