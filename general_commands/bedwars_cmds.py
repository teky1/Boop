import os
import discord
from datetime import datetime, time, timedelta
import calendar
from discord.ext import commands
import utilities.hypixel_utils as hypixel

async def _bwquests(ctx: commands.Context, ign):
    quest_data = hypixel.getBwQuestData(ign)
    embed = discord.Embed(title="Bedwars Quests", color=0x00ff4c)
    embed.set_thumbnail(url="https://hypixel.net/styles/hypixel-v2/images/game-icons/BedWars-64.png")

    last_midnight = datetime.combine(datetime.today(), time.min).timestamp()
    last_friday = datetime.today()

    while last_friday.weekday() != calendar.FRIDAY:
        last_friday -= timedelta(days=1)
    last_friday = datetime.combine(last_friday, datetime.min.time()).timestamp()


    if "active" not in quest_data["bedwars_daily_win"]:
        last_completion = quest_data["bedwars_daily_win"]["completions"][-1]["time"]/1000
        if last_completion > last_midnight:
            daily_win_value = "🟢 (1/1 Wins)"
        else:
            daily_win_value = "🔴 Not Started"
    elif quest_data["bedwars_daily_win"]["active"]["objectives"] == {}:
        daily_win_value = "🔴 (0/1 Wins)"

    if "active" not in quest_data["bedwars_daily_one_more"]:
        last_completion = quest_data["bedwars_daily_one_more"]["completions"][-1]["time"]/1000
        if last_completion > last_midnight:
            daily_one_more_value = "🟢 (2/2 Games)"
        else:
            daily_one_more_value = "🔴 Not Started"
    elif quest_data["bedwars_daily_one_more"]["active"]["objectives"] == {}:
        daily_one_more_value = "🔴 (0/2 Games)"
    else:
        daily_one_more_value = "🟡 (1/2 Games)"

    if "active" not in quest_data["bedwars_weekly_bed_elims"]:
        last_completion = quest_data["bedwars_weekly_bed_elims"]["completions"][-1]["time"]/1000
        if last_completion > last_friday:
            weekly_beds = "🟢 (25/25 Beds)"
        else:
            weekly_beds = "🔴 Not Started"
    elif quest_data["bedwars_weekly_bed_elims"]["active"]["objectives"] == {}:
        weekly_beds = "🔴 (0/25 Beds)"
    else:
        bed_count = quest_data["bedwars_weekly_bed_elims"]["active"]["objectives"]["bedwars_bed_elims"]
        weekly_beds = f"🟡 ({bed_count}/25 Beds)"

    if "active" not in quest_data["bedwars_weekly_dream_win"]:
        last_completion = quest_data["bedwars_weekly_dream_win"]["completions"][-1]["time"]/1000
        if last_completion > last_friday:
            weekly_dream_wins = "🟢 (10/10 Wins)"
        else:
            weekly_dream_wins = "🔴 Not Started"
    elif quest_data["bedwars_weekly_dream_win"]["active"]["objectives"] == {}:
        weekly_dream_wins = "🔴 (0/10 Wins)"
    else:
        bed_count = quest_data["bedwars_weekly_dream_win"]["active"]["objectives"]["bedwars_dream_wins"]
        weekly_dream_wins = f"🟡 ({bed_count}/10 Wins)"

    embed.add_field(name=f"Weekly Beds\n{weekly_beds}",
                    value=f"{len(quest_data['bedwars_weekly_bed_elims']['completions'])} completions", inline=False)
    embed.add_field(name=f"Weekly Dream Wins\n{weekly_dream_wins}",
                    value=f"{len(quest_data['bedwars_weekly_dream_win']['completions'])} completions", inline=False)

    # embed.add_field(name="\u200b", value="\u200b", inline=False)

    embed.add_field(name=f"Daily Win\n{daily_win_value}",
                    value=f"{len(quest_data['bedwars_daily_win']['completions'])} completions", inline=False)
    embed.add_field(name=f"Daily Games\n{daily_one_more_value}",
                    value=f"{len(quest_data['bedwars_daily_one_more']['completions'])} completions", inline=False)





    await ctx.send(embed=embed)