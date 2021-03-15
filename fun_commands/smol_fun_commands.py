import discord
from discord.ext import commands


async def _boop(ctx, who: discord.User):
    if who is None:
        await ctx.send("Who u boopin???")
        return

    await ctx.send(who.mention+" ***YOU*** have been booped!!!!!!")


async def _repeat(ctx):
    async with ctx.typing():
        if len(str(ctx.message.content)) > 9:
            if ctx.message.mention_everyone:
                message = discord.utils.escape_mentions(str(ctx.message.content)[8:])
            else:
                message = str(ctx.message.content)[8:]
            await ctx.send(message)


async def _say(ctx):
    async with ctx.typing():
        if len(str(ctx.message.content)) > 6:
            if ctx.message.mention_everyone:
                message = discord.utils.escape_mentions(str(ctx.message.content)[5:])
            else:
                message = str(ctx.message.content)[5:]
            await ctx.send(message)
        await ctx.message.delete()
