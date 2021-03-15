import discord
from discord.ext import commands

async def _boop(ctx, who: discord.User):
    if who is None:
        await ctx.send("Who u boopin???")
        return

    await ctx.send(who.mention+" ***YOU*** have been booped!!!!!!")