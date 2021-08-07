import discord
import math
from utilities.hypixel_utils import getFriends, returnUUID, returnName

async def _mutuals(ctx, person1, person2, page):

    msg = await ctx.reply("Loading...")

    person1_friends = getFriends(returnUUID(person1))
    person2_friends = getFriends(returnUUID(person2))

    mutual_uuids = []

    for friend in person1_friends:
        if friend in person2_friends:
            mutual_uuids.append(friend)

    if len(mutual_uuids) == 0:
        await ctx.reply("These two people have no mutual friends :P")
        return

    page_count = math.ceil(len(mutual_uuids)/15)
    current_page = mutual_uuids[15*(page-1):page*15]

    message = f"**Mutual Friends Page ({page}/{page_count}):**\n"

    for person in current_page:
        message += f"{returnName(person)}\n"

    if page_count > 1 and page != page_count:
        message += f"*`!mutuals {person1} {person2} {page+1}` to see Page {page+1}.*"

    await msg.edit(content=message)

