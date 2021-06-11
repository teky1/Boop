import discord
import json
import random
import requests
import string
from discord_components import Button, ButtonStyle
import utilities.equation_interpreter as interpreter
import utilities.webhook_utils as webhooks

with open("data/boop_gifs.txt") as file:
    boop_gifs = file.read().split()

async def _boop(ctx, who: discord.User):
    if who is None:
        await ctx.send("Who u boopin???")
        return
    embed = discord.Embed(description=who.mention+" ***YOU*** have been booped!!!!!!")
    print(boop_gifs)
    embed.set_image(url=random.choice(boop_gifs))
    await ctx.send(embed=embed)



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

async def isHelloTarget(person1, person2, interaction):
    if person1 == person2:
        return True
    else:
        await interaction.respond

async def _hello(ctx, client):
    # async with ctx.typing():
    #     await ctx.send("heyyy world ;)")
    # return

    goodButton = Button(label="I'm doing good!",  style=ButtonStyle.green, emoji="😁")
    badButton = Button(label="I'm doing bad!", style=ButtonStyle.red, emoji="😔")
    mehButton = Button(label="I'm doing meh..", style=ButtonStyle.grey, emoji="😕")
    idkButton = Button(label="idek bro lmao", style=ButtonStyle.blue, emoji="🤷‍♂️")
    response = await ctx.reply("Hello! How are you doing today?", components=[[
        goodButton,
        badButton
    ],
    [
        mehButton,
        idkButton
    ]])
    interactionRecieved = False
    while interactionRecieved is False:
        interaction = await client.wait_for("button_click", check=lambda i : i.component.id in [goodButton.id, badButton.id, mehButton.id, idkButton.id])

        if interaction.message.mentions[0] == interaction.author:
            interactionRecieved = True
        else:

            await interaction.respond(content="I don't remember asking *you* :/")
            print("roasted " + str(interaction.author))

    if interaction.component.id == goodButton.id:
        await interaction.respond(content="That's good to hear!", ephemeral=False)
    elif interaction.component.id == badButton.id:
        await interaction.respond(content="Oh no! Hope you feel better!", ephemeral=False)
    elif interaction.component.id == mehButton.id:
        await interaction.respond(content="We all have those days :/", ephemeral=False)
    elif interaction.component.id == idkButton.id:
        await interaction.respond(content="damn", ephemeral=False)

    goodButton.disabled = True
    badButton.disabled = True
    mehButton.disabled = True
    idkButton.disabled = True

    await response.edit(components=[[
        goodButton,
        badButton
    ],
    [
        mehButton,
        idkButton
    ]])

async def _upsidedown(ctx):
    message = " ".join(ctx.message.content.split()[1:])
    flipped_chars = "Z⅄XMΛ∩⊥SᴚΌԀONW˥⋊ſIH⅁ℲƎ◖Ɔ𐐒∀zʎxʍʌnʇsɹbdouɯןʞɾıɥƃɟǝpɔqɐ"[::-1]
    reversed_msg = list(message[::-1])
    for i,char in enumerate(reversed_msg):
        if char in string.ascii_letters:
            reversed_msg[i] = flipped_chars[string.ascii_letters.index(char)]
    await webhooks.sendWebhook(ctx.channel, ctx.author.display_name, ctx.author.avatar_url, "".join(reversed_msg))
    await ctx.message.delete()


async def _fancy(ctx):
    message = list(" ".join(ctx.message.content.split()[1:]))
    fancy_font = '𝒶𝒷𝒸𝒹𝑒𝒻𝑔𝒽𝒾𝒿𝓀𝓁𝓂𝓃𝑜𝓅𝓆𝓇𝓈𝓉𝓊𝓋𝓌𝓍𝓎𝓏𝒜𝐵𝒞𝒟𝐸𝐹𝒢𝐻𝐼𝒥𝒦𝐿𝑀𝒩𝒪𝒫𝒬𝑅𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵'
    for i,char in enumerate(message):
        if char in string.ascii_letters:
            message[i] = fancy_font[string.ascii_letters.index(char)]
    await webhooks.sendWebhook(ctx.channel, ctx.author.display_name, ctx.author.avatar_url, "".join(message))
    await ctx.message.delete()

async def _wide(ctx):
    message = list(" ".join(ctx.message.content.split()[1:]))
    fancy_font = 'ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ'
    for i,char in enumerate(message):
        if char in string.ascii_letters:
            message[i] = fancy_font[string.ascii_letters.index(char)]
    await webhooks.sendWebhook(ctx.channel, ctx.author.display_name, ctx.author.avatar_url, "".join(message))
    await ctx.message.delete()

async def _namemc(ctx):
    async with ctx.typing():
        parameters = ctx.message.content.split()
        if len(parameters) <= 1:
            await ctx.send("give ign :)")
            return
        await ctx.send(f"https://namemc.com/profile/{parameters[1]}")
    return