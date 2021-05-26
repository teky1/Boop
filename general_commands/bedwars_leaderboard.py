import random
import utilities.equation_interpreter as interpreter
import utilities.hypixel_utils as hypixel
import matplotlib.pyplot as plt
import os
import discord

async def _bwterms(ctx):
    await ctx.send("**OVERALL DATA:**\n\nlevel (star), wins (w), losses (l), final_kills (fk), final_deaths (fd), kills (k), deaths (d), beds_broken (bb), beds_lost (bl)\n\n"
                   "**SPECIFIC MODES:**\n\nFormat: gametype\\_stat\n"
                   "For example, to get solo wins you would do solo_w or to get fours bed breaks you would do fours_bb.\n(gametypes are: solo, doubles, threes, fours)\n"
                   "\n**Note:** Full stat names such as wins and final_kills cannot be used for specific modes, their abbreviations must be used (w and fk)\n"
                   )

async def _bwscore(ctx, ign, equation):
    values = hypixel.getIGNBwStats(ign)
    score = round(float(interpreter.interpret(values, equation)), 2)
    op = "```\nBed Wars\n"
    op += f"Equation: {equation}\n"
    op += f"{ign}: {score}\n```"
    await ctx.send(op)


async def _bedwarsleaderboard(ctx, equation):
    async with ctx.typing():
        with open("data/registered_players.txt", "r") as player_file:
            contents = player_file.read().split()
        all_stats = hypixel.getAllPlayerBwStats(contents)
        lb = leaderboard(all_stats, equation)
        output = f"```\nBed Wars\n{equation} leaderboards:\n"

        total_sum = 0

        for i in range(len(lb)):
            output+=f"{i+1}. {lb[i][0]} ({lb[i][1]})\n"
            total_sum += lb[i][1]

        if ctx.message.content.lower().endswith("-s"):
            output += "\nTotal Sum: "+str(total_sum)+"\n"
        elif ctx.message.content.lower().endswith("-a"):
            output += "\nAverage: " + str(round(total_sum/len(lb), 3))+"\n"

        output += "```"
        await ctx.send(output)

async def _graphleaderboard(ctx, equation):
    async with ctx.typing():

        temp_id = str(round(random.random()*100000))+".png"

        with open("data/registered_players.txt", "r") as player_file:
            contents = player_file.read().split()
        all_stats = hypixel.getAllPlayerBwStats(contents)
        lb = leaderboard(all_stats, equation)

        names = [x[0] for x in lb[::-1]]
        scores = [x[1] for x in lb[::-1]]

        plt.clf()
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.barh(names, scores, color="white")
        plt.title(f'{equation}', color="white")
        plt.tight_layout()

        ax.spines['bottom'].set_color('white')
        ax.spines['top'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.spines['right'].set_color('white')
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')

        plt.savefig(temp_id, transparent=True)
        await ctx.send(file=discord.File(temp_id))
        os.remove(temp_id)




# The following are functions only used in this file for leaderboard stuff so i didnt put it in utils

def scoreFromList(list):
    return list[1]

def leaderboard(player_data, equation):
    scores = []
    for person in player_data:
        try:
            score = round(float(interpreter.interpret(player_data[person], equation)), 2)
        except ZeroDivisionError:
            score = 0.0
        scores.append([person, score])
    scores = sorted(scores, key=scoreFromList, reverse=True)
    return scores