import discord
import utilities.equation_interpreter as interpreter
from discord.ext import commands

async def _boop(ctx, who: discord.User):
    if who is None:
        await ctx.send("Who u boopin???")
        return

    await ctx.send(who.mention+" ***YOU*** have been booped!!!!!!")

async def _calc(ctx):
    args = ctx.message.content.split()
    if len(args) == 1:
        await ctx.send("**Correct Format**: !calc <equation>\n\n"
                       "*This command is used to make/test basic PEMDAS calculations using Ortho's equation interpreter.*")

    equation = ctx.message.content.replace("!calc ", "", 1)

    answer = round(float(interpreter.interpret(values={}, equation=equation)), 4)

    await ctx.send(f"```\n{equation}\nAnswer: {answer}\n```")