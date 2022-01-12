import random


async def process_gavin(message):
    response = "gavin so i am the stinkiest person ever"
    stinky = message.content.replace("'", "").replace("-", "").replace(".", "").upper().strip()
    if stinky == "I":
        await message.channel.send("am "+response)
    elif stinky in ["IM", "I AM"]:
        await message.channel.send(response)

async def process_grass(message):
    response = "mommy grass"
    stinky = message.content.replace("'", "").replace("-", "").replace(".", "").upper().strip()
    if stinky == "I":
        await message.channel.send("am " + response)
    elif stinky in ["IM", "I AM"]:
        await message.channel.send(response)

async def process_hiley(message):
    response = "big man sugar daddy. u can call me ~~hiley~~ hailey tho"
    stinky = message.content.replace("'", "").replace("-", "").replace(".", "").upper().strip()
    if stinky == "I":
        await message.channel.send("am " + response)
    elif stinky in ["IM", "I AM"]:
        await message.channel.send(response)

async def process_lauren(message):
    response = "#LUREEN2024"
    stinky = message.content.replace("'", "").replace("-", "").replace(".", "").upper().strip()
    if stinky == "I":
        await message.channel.send("am " + response)
    elif stinky in ["IM", "I AM"]:
        await message.channel.send(response)

async def process_brian(message):
    response = random.choice(["got my drivers license last week",
                           "hope you're happy but dont be happier",
                           "hope i was your favorite crime",
                           "know you get deja vu",
                           "guess you moved on really easily"])
    stinky = message.content.replace("'", "").replace("-", "").replace(".", "").upper().strip()
    if stinky == "I":
        await message.channel.send(response)

async def process_default(message):
    stinky = message.content.replace("'", "").replace("-", "").replace(".", "").upper().strip()
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

special = {
    524331117516554253: process_gavin,
    720288689141579776: process_grass,
    335958694585958400: process_hiley,
    471313677618774031: process_lauren,
    217753105276600320: process_brian,
}