import discord
import utilities.hypixel_utils as hypixel

async def _online(ctx):
    async with ctx.typing():

        with open("data/registered_players.txt", "r") as player_file:
            contents = player_file.read().split()
        try:
            hypixel_peeps = hypixel.check(contents)
        except KeyError:
            await ctx.send("Sorry, there's too many API requests right now. Please wait ~1 minute before trying again")
            return

        if hypixel_peeps == False:
            await ctx.send("Sorry, there's too many API requests right now. Please wait 1 minute before trying again")
            return

        embed = discord.Embed(title="Hypixel", color=0x00ff4c)
        embed.set_thumbnail(url="https://hypixel.net/attachments/hypixel-jpg.760131/")
        for dude in hypixel_peeps:
            embed.add_field(name=f"🟢 {dude[0]}", value=f"{dude[1]}\n{dude[2]}", inline=True)
        if len(hypixel_peeps) == 0:
            embed.add_field(name=f"hmmm", value=f"nobody online :(", inline=False)

        if len(hypixel_peeps) > 0:
            await ctx.send(embed=embed)
        else:
            await ctx.send("Nobody on Hypixel :((")