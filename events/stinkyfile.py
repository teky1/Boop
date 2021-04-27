import random


async def stink(message):
    stinky = message.content.replace("'", "").replace("-", "").replace(".", "").upper()

    if "┻━┻" in message.content:
        await message.channel.send("┬─┬ ノ( ゜-゜ノ) "*message.content.count('┻━┻'))
    elif message.author.id == 524331117516554253 and stinky not in ["you", "u", "youre", "your", "ur"]:
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