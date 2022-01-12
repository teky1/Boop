import random
import math
import re

async def stink(message):
    stinky = message.content.replace("'", "").replace("-", "").replace(".", "").upper()


    if message.author.id == 524331117516554253 and stinky not in ["you", "u", "youre", "your", "ur"]:
        if stinky == "I":
            await message.channel.send("am gavin so i am the stinkiest person ever")
        elif stinky == "IM" or stinky == "I AM":
            await message.channel.send("gavin so i am the stinkiest person ever")
    elif message.author.id == 720288689141579776 and stinky not in ["you", "u", "youre", "your", "ur"]:
        if stinky == "I":
            await message.channel.send("am mommy grass")
        elif stinky == "IM" or stinky == "I AM":
            await message.channel.send("mommy grass")
    elif message.author.id == 335958694585958400 and stinky not in ["you", "u", "youre", "your", "ur"]:
        if stinky == "I":
            await message.channel.send("am big man sugar daddy. u can call me ~~hiley~~ hailey tho")
        elif stinky == "IM" or stinky == "I AM":
            await message.channel.send("big man sugar daddy. u can call me ~~hiley~~ hailey tho")
    elif message.author.id == 471313677618774031 and stinky not in ["you", "u", "youre", "your", "ur"]:
        if stinky == "I":
            await message.channel.send("am #LUREEN2021")
        elif stinky == "IM" or stinky == "I AM":
            await message.channel.send("#LUREEN2021")
    elif message.author.id == 217753105276600320 and stinky not in ["you", "u", "youre", "your", "ur", "IM", "I AM"]: # special for brian
        brian = random.choice(["got my drivers license last week",
                            "hope you're happy but dont be happier",
                            "hope i was your favorite crime",
                            "know you get deja vu",
                            "guess you moved on really easily"])
        if stinky == "I":
            await message.channel.send(brian)
        # elif stinky == "IM" or stinky == "I AM":
            # await message.channel.send(brian)
    elif random.randint(0, 1):
        if stinky == "I":
            if random.randint(0, 2):
                await message.channel.send("am stinky")
            else:
                await message.channel.send("am so hot")
        elif stinky == "IM" or stinky == "I AM":
            if random.randint(0, 2):
                await message.channel.send("stinky")
            else:
                await message.channel.send("so hot")

        if stinky == "you" or stinky == "u":
            if random.randint(0, 2):
                await message.channel.send("are stinky.")
            else:
                await message.channel.send("are so hot")
        elif stinky == "youre" or stinky == "ur" or stinky == "you are":
            if random.randint(0, 2):
                await message.channel.send("stinky.")
            else:
                await message.channel.send("so hot")

    if message.content == "yes" and message.author.id == 668143289651691530:
        await message.channel.send("no")

    elif random.randint(1, 1000) == 420:
        await message.channel.send("^")

    if message.content == "but":
        await message.channel.send("t")

    if re.match('\Ayo+u+$|\Au+$', message.content.lower()) is not None:
        await message.channel.send("soulja boy tell ya")

    legTypes = "┻⊥丄⏊┴ㅗ上⅃"
    totalLegs = 0
    for x in legTypes:
        totalLegs += message.content.count(x)
    if totalLegs > 0  and not message.author.bot:
        await message.channel.send("┬─┬ ノ( ゜-゜ノ) "*math.ceil(totalLegs/2))
    if message.author.id == 836946432186384404 and message.content == "go to class olds :D":
        await message.channel.send("shut up carl")
