import json
import discord
from gaming.connectfour import fetchu
from time import localtime


async def _birthdays(ctx, client):
    with open("data/birthdays.json") as in_file:
        filedata = json.load(in_file)
    embed = discord.Embed(title="Registered Birthdays:", description=f"**{94 * '-'}**", color=0x97f575)
    for each in range(len(filedata["author"])):
        if filedata["month"][each] == 12 or filedata["month"][each] <= 2:
            emoji = "❄️"
        elif filedata["month"][each] <= 5:
            emoji = "🌱️"
        elif filedata["month"][each] <= 8:
            emoji = "☀️"
        else:
            emoji = "🍂"
        embed.add_field(name=f"{emoji} {await fetchu(filedata['author'][each], client)}",
                        value=f'{filedata["month"][each]}/{filedata["day"][each]}/{filedata["year"][each]}', inline=True)
    await ctx.send(embed=embed)



async def _birth(ctx, client):
    msgdata = str(ctx.message.content)[7:]
    validdays = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
    try:
        author = await fetchu(ctx.message.raw_mentions[0], client)
        author = author.id
    except IndexError:
        author = ctx.author.id
    try:
        month = int(msgdata.split("/")[0])
        day = int(msgdata.split("/")[1])
        year = int(msgdata.split("/")[2].split()[0])
        if month > 12:
            await ctx.send("this is not a valid month.")
            return
        if day > validdays[month] and not year % 4 == 0 and not month == 2 and not day == 29:
            await ctx.send("this is not a valid day.")
            return
        if year < 1000:
            await ctx.send("four digit year pls ;)")
            return
        if year < 2000:
            await ctx.send("ok smol")
            return
    except IndexError:
        await ctx.send("provide a valid birthday (mm/dd/yyyy)")
        return
    except ValueError:
        await ctx.send("provide a valid birthday (mm/dd/yyyy)")
        return

    with open("data/birthdays.json") as in_file:
        filedata = json.load(in_file)

    if author not in filedata["author"]:
        filedata["month"].append(month)
        filedata["day"].append(day)
        filedata["year"].append(year)
        filedata["author"].append(author)
    else:
        ind = filedata["author"].index(author)
        filedata["month"][ind] = month
        filedata["day"][ind] = day
        filedata["year"][ind] = year

    with open("data/birthdays.json", "w") as out_file:
        json.dump(filedata, out_file, indent=4)
    await ctx.send("birthday saved :D")



async def _nextbirth(ctx, client): # assumes no twins
    with open("data/birthdays.json") as in_file:
        filedata = json.load(in_file)
    validdays = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
    daysaway = []
    today = int(localtime().tm_yday)
    for entry in range(len(filedata["month"])):
        yeardate = 0
        for month in range(filedata["month"][entry]):
            if not month == 0:
                yeardate = yeardate + validdays[month]
        daysaway.append(yeardate + filedata["day"][entry] - today)
    beforesort = []
    for number in daysaway:
        beforesort.append(number)
    daysaway.sort()
    for boop in daysaway:
        if boop >= 0:
            ind = beforesort.index(boop)
            age = int(localtime().tm_year) - filedata["year"][ind]
            name = await fetchu(filedata['author'][ind], client)
            name = str(name)[:-5]
            await ctx.send(f'The next registered birthday is:\n{name} (turning {age}) on '
                           f'{filedata["month"][ind]}/{filedata["day"][ind]}/{filedata["year"][ind]}')
            break
