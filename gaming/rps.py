from gaming.gamestart import duelstart
import json


async def _rps(ctx, client, games):
    result = await duelstart(ctx, "Rock Paper Scissors", client)
    if result == 0:
        return
    challenger = result[0]
    challenged = result[1]
    await ctx.send(f"{challenged} accepted the duel! Check your dms!")
    challenger_message = await challenger.send(f"{challenger} vs {challenged} \n you have 10 seconds to respond")
    challenged_message = await challenged.send(f"{challenger} vs {challenged} \n you have 10 seconds to respond")
    game_messages = [[ctx, challenger, challenged, "rps"], challenger_message, challenged_message]
    games.games.append(game_messages)
    emojis = ["🗿", "📝", "✂"]
    for message in game_messages[1:]:
        for emoji in emojis:
            await message.add_reaction(emoji)
    return game_messages


async def rpsgame(payload, game):
    rpsemojis = ["🗿", "📝", "✂"]
    emojinames = ["rock", "paper", "scissors"]
    winningcases = ["paperrock", "rockscissors", "scissorspaper"]
    for message in game[1:]:
        if message not in emojinames and payload.message_id == message.id and str(payload.emoji) in rpsemojis \
                and payload.user_id != 811435588942692352:
            for thing in range(len(game[1:])):
                try:
                    if game[thing+1].id == payload.message_id:
                        game[thing+1] = emojinames[rpsemojis.index(str(payload.emoji))]
                except AttributeError:
                    pass
            if game[1] in emojinames and game[2] in emojinames:
                with open("data/rockpaperscissorstats.json") as in_file:
                    stats = json.load(in_file)
                if str(game[0][1].id) not in stats:
                    stats[str(game[0][1].id)] = {"wins": 0, "ties": 0, "losses": 0,
                                                 "rock": 0, "paper": 0, "scissors": 0}
                if str(game[0][2].id) not in stats:
                    stats[str(game[0][2].id)] = {"wins": 0, "ties": 0, "losses": 0,
                                                 "rock": 0, "paper": 0, "scissors": 0}
                stats[str(game[0][1].id)][game[1]] += 1
                stats[str(game[0][2].id)][game[2]] += 1
                if game[1] == game[2]:
                    who_won = f"<@!{game[0][1].id}> and <@!{game[0][2].id}> tied " \
                              f"in their duel {rpsemojis[emojinames.index(game[1])]}!"
                    stats[str(game[0][1].id)]["ties"] += 1
                    stats[str(game[0][2].id)]["ties"] += 1
                elif game[1] + game[2] in winningcases:
                    who_won = f"<@!{game[0][1].id}> {rpsemojis[emojinames.index(game[1])]} won the duel against " \
                              f"<@!{game[0][2].id}> {rpsemojis[emojinames.index(game[2])]}!"
                    stats[str(game[0][1].id)]["wins"] += 1
                    stats[str(game[0][2].id)]["losses"] += 1
                else:
                    who_won = f"<@!{game[0][2].id}> {rpsemojis[emojinames.index(game[2])]} won the duel against " \
                              f"<@!{game[0][1].id}> {rpsemojis[emojinames.index(game[1])]}!"
                    stats[str(game[0][1].id)]["losses"] += 1
                    stats[str(game[0][2].id)]["wins"] += 1
                await game[0][0].send(who_won)
                with open("data/rockpaperscissorstats.json", "w") as out_file:
                    json.dump(stats, out_file, indent=4)


async def _duelstats(ctx, client):
    async with ctx.typing():
        if len(ctx.message.raw_mentions) == 0:
            player = ctx.message.author
        else:
            player = await client.fetch_user(ctx.message.raw_mentions[0])
        with open("data/rockpaperscissorstats.json") as in_file:
            stats = json.load(in_file)
        try:
            stats = stats[str(player.id)]
        except KeyError:
            await ctx.send("This player has no stats!")
            return
        games = stats['wins'] + stats['losses'] + stats['ties']
        statgames = stats['rock'] + stats['paper'] + stats['scissors']
        statmessage = f"<@!{player.id}>'s 🗿📝✂ stats:\n" \
                      f"They have played {games} total games.\n \n" \
                      f"Wins: {stats['wins']} ({round(100*stats['wins']/games)}%)\n" \
                      f"Ties: {stats['ties']} ({round(100*stats['ties']/games)}%)\n" \
                      f"Losses: {stats['losses']} ({round(100 * stats['losses']/games)}%)\n \n" \
                      f"Rocks: {stats['rock']} ({round(100*stats['rock']/statgames)}%)\n" \
                      f"Papers: {stats['paper']} ({round(100*stats['paper']/statgames)}%)\n" \
                      f"Scissors: {stats['scissors']} ({round(100*stats['scissors']/statgames)}%)\n"
        await ctx.send(statmessage)