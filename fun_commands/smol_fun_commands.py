from __future__ import print_function
import os
import discord
from discord.ext import commands
import json
import string
from PIL import Image, ImageDraw, ImageFont, ImageOps
from io import BytesIO
import requests
import random
import colorsys
from discord_components import Button, ButtonStyle
import utilities.equation_interpreter as interpreter
import utilities.webhook_utils as webhooks
import MinePI

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

async def _kiera(ctx):
    ranks_gifted = requests.get("https://api.hypixel.net/player?key=8803f760-c698-43c9-b469-f0a6594f963a&uuid=7916fac35c824198b0043ef4cfd8055c").json()
    ranks_gifted = ranks_gifted["player"]["giftingMeta"]["ranksGiven"]
    await ctx.send(f"Kiera has gifted **{ranks_gifted}** frikin ranks1!! dm her and tell her to stop :)")

async def _sumograss(ctx: commands.Context):
    data = requests.get("https://api.hypixel.net/player?key=8803f760-c698-43c9-b469-f0a6594f963a&uuid=a6e830d4-766c-4288-a650-04c65c5dfa29").json()
    wins = data["player"]["stats"]["Duels"]["sumo_duel_wins"]

    im = Image.open("data/image_tings/top1.png")
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype("data/image_tings/Lato-Black.ttf", 65)
    draw.text((130, 100), str(wins), (255, 255, 255), font=font)
    # print(im.format, im.size, im.mode)
    name = str(random.randint(0, 999999)) + ".png"
    im.save(name)
    await ctx.send(file=discord.File(name))
    os.remove(name)

async def _spoopyskin(ctx: commands.Context, name):
    uuid = requests.get("https://api.mojang.com/users/profiles/minecraft/" + name).json()["id"]
    skin_req = requests.get(f"https://crafatar.com/skins/{uuid}")
    gray_skin_img = Image.open(BytesIO(skin_req.content)).convert("RGB")
    skin_mask = Image.open(BytesIO(skin_req.content))


    skin_data = gray_skin_img.load()

    for x in range(gray_skin_img.size[0]):
        for y in range(gray_skin_img.size[1]):
            px = skin_data[x, y]
            px = list(colorsys.rgb_to_hsv(px[0]/255, px[1]/255, px[2]/255))
            px[0] = (px[0]+0.5) % 1
            px = colorsys.hsv_to_rgb(px[0], px[1], px[2])
            skin_data[x, y] = (int(px[0]*255), int(px[1]*255), int(px[2]*255))


    gray_skin_img = ImageOps.grayscale(gray_skin_img)
    pompkin = Image.open("data/image_tings/pompkin.png").convert("RGBA")

    skin_img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    skin_img.paste(gray_skin_img, (0, 0), skin_mask)
    skin_img.paste(pompkin, (42, 8), pompkin)

    render = await MinePI.render_3d_skin(skin_image=skin_img)
    render.save("render.png")
    skin_img.save("spoopyskin.png")
    await ctx.send(content="**Skin File:**", files=[discord.File("spoopyskin.png"),discord.File("render.png")])
    os.remove("spoopyskin.png")
    os.remove("render.png")


