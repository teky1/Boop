import discord
import json
import random
import requests
import utilities.equation_interpreter as interpreter


async def _boop(ctx, who: discord.User):
    if who is None:
        await ctx.send("Who u boopin???")
        return

    await ctx.send(who.mention+" ***YOU*** have been booped!!!!!!")



async def _repeat(ctx):
    async with ctx.typing():
        if len(str(ctx.message.content)) > 8:
            if ctx.message.mention_everyone:
                message = discord.utils.escape_mentions(str(ctx.message.content)[7:])
            else:
                message = str(ctx.message.content)[7:]
            await ctx.send(message)


async def _say(ctx):
    async with ctx.typing():
        if len(str(ctx.message.content)) > 5:
            if ctx.message.mention_everyone:
                message = discord.utils.escape_mentions(str(ctx.message.content)[4:])
            else:
                message = str(ctx.message.content)[4:]
            await ctx.send(message)
        await ctx.message.delete()


async def _calc(ctx):
    args = ctx.message.content.split()
    if len(args) == 1:
        await ctx.send("**Correct Format**: !calc <equation>\n\n"
                       "*This command is used to make/test basic PEMDAS calculations using Ortho's equation interpreter.*")

    equation = ctx.message.content.replace("!calc ", "", 1)

    answer = round(float(interpreter.interpret(values={}, equation=equation)), 4)

    await ctx.send(f"```\n{equation}\nAnswer: {answer}\n```")


async def _quote(ctx):
    names = ctx.message.content.split()[1:]
    placeholders = ["{A}", "{B}", "{C}", "{D}", "{E}", "{F}"]
    with open("data/quotes.json", encoding="utf8") as json_file:
        quote_list = json.load(json_file)["quotes"][len(names) - 1]

    header = "**ScatterPatter's Incorrect Quotes Generator**\n\n"
    quote = quote_list[random.randint(0, len(quote_list) - 1)]
    quote = quote.replace("<br>", "\n")
    quote = quote.replace("*", "\\*")
    quote = quote.replace("<i>", "*")
    quote = quote.replace("</i>", "*")
    for i, item in enumerate(placeholders):
        if quote.count(item) > 0:
            quote = quote.replace(item, f"{names[i]}")
    quote = header + quote
    # embed = discord.Embed(title="ScatterPatter's Incorrect Quotes Generator",
    #                       url="https://incorrect-quotes-generator.neocities.org/",
    #                       description=quote)
    # embed.add_field(name=quote, value="Check out the website :D", inline=True)

    quote += f"\n\nAll quotes taken from: https://incorrect-quotes-generator.neocities.org/"
    await ctx.send(quote)

async def _cat(ctx):
    result = requests.get("https://api.thecatapi.com/v1/images/search").json()[0]
    await ctx.send(result["url"])


async def _simp(ctx):
    async with ctx.typing():
        dream = str(ctx.message.content)[6:].upper()
        if len(dream) > 0:
            await ctx.send(f"{dream}‼️{dream}‼️ Hello 😀👋🏻 do your shoes need shining? 🤔👟✨ \n"
                           f"{dream}😳‼️{dream} please 🥺☹️🙏 Should you need coffee? 👀☕️ \n"
                           f"Come back 😫 PLEASE my clout 😤🤑 Dont go away from me 🥺\n{dream} Please 😫😫🤨")
        else:
            await ctx.send("!simp needs a subject to simp for")


async def _hello(ctx):
    async with ctx.typing():
        await ctx.send("heyyy world ;)")
    return