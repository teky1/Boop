import utilities.equation_interpreter as interpreter
import utilities.hypixel_utils as hypixel

async def _bwterms(ctx):
    await ctx.send("The available data for BW is: level (star), wins (w), losses (l), final_kills (fk), final_deaths (fd), kills (k), deaths (d), beds_broken (bb), beds_lost (bl)")

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