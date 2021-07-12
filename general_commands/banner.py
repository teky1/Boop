import discord
from discord.ext import commands
from PIL import Image
from PIL import ImageDraw
import random
import requests
from utilities.banner_utils import importmenoballs as placer

SCALING_SIZE = 3
STATUSES = ["data/banner_stuff/resources/idle", "data/banner_stuff/resources/dnd", "data/banner_stuff/resources/online"]
def createPfpThing(status, pfp_path):
    #statuses: online, dnd, idle
    img = Image.open(pfp_path).resize((512,512)).convert(mode="RGBA")
    status_img = Image.open(f"{status}.png").resize((100, 100))
    transparent_background = Image.new('RGBA', (512, 512), (0, 0, 0, 0))

    mask = Image.new("1", (512, 512), 1)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0, 512, 512), fill=0)
    mask_draw.ellipse((346, 346, 524, 524), fill=1)

    img = Image.composite(transparent_background, img, mask)
    img.paste(status_img, (381, 381), status_img)

    return img


async def doTheThing(pfp_path, message):
    image_path = f"data/banner_stuff/temp/{random.randrange(5, 1000000)}.png"
    locations = await placer(message)
    print("starting image process")
    locations = [[z*SCALING_SIZE for z in x] for x in locations]
    background = Image.new("RGBA", (600*SCALING_SIZE, 240*SCALING_SIZE), (24, 25, 28, 255))
    for pfp in locations:
        pfp_img = createPfpThing(random.choice(STATUSES), pfp_path).resize((pfp[0]*2, pfp[0]*2))
        background.paste(pfp_img, (int(pfp[1])-pfp[0], int(pfp[2])-pfp[0]), pfp_img)
    background.save(image_path)
    return image_path


async def _banner(ctx: commands.Context, person):
    target = person
    message = await ctx.reply("Loading... (This could take a lil bit so)")
    avatar_url = str(target.avatar_url_as(format="png", size=512))
    resp = requests.get(avatar_url)
    with open(f"data/banner_stuff/temp/{target.id}.png", "wb") as pfp_file:
        pfp_file.write(resp.content)

    output = await doTheThing(f"data/banner_stuff/temp/{target.id}.png", message)
    await ctx.send(file=discord.File(output), content="")
    await message.delete()
