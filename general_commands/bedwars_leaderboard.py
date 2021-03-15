import utilities.equation_interpreter as interpreter
import utilities.hypixel_utils as hypixel

async def _bwterms(ctx):
    await ctx.send("The available data for BW is: level, wins, losses, final_kills, final_deaths, kills, deaths, "
                   "beds_broken, beds_lost")

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

        for i in range(len(lb)):
            output+=f"{i+1}. {lb[i][0]} ({lb[i][1]})\n"
        output += "```"
        await ctx.send(output)

# The following are functions only used in this file for leaderboard stuff so i didnt put it in utils

def scoreFromList(list):
    return list[1]

def leaderboard(player_data, equation):
    scores = []
    for person in player_data:
        score = round(float(interpreter.interpret(player_data[person], equation)), 2)
        scores.append([person, score])
    scores = sorted(scores, key=scoreFromList, reverse=True)
    return scores