import random
import math
import re
import events.iMessages as iMessages

async def stink(message):
    stinky = message.content.replace("'", "").replace("-", "").replace(".", "").upper()

    if message.author.id in iMessages.special:
        await iMessages.special[message.author.id](message)
    else:
        await iMessages.process_default(message)

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
