import random


async def stink(message):
    stinky = message.content.replace("'", "").replace("-", "").replace(".", "").upper()

    if random.randint(0, 1):
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

    if random.randint(0, 1):
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