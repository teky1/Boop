async def duelstart(ctx, game):
    if str(ctx.message.channel)[:len("Direct Message with")] == "Direct Message with":
        await ctx.send("no duels in dms!")
        return 0
    parameters = ctx.message.content.split()
    challenger = ctx.author
    if len(parameters) <= 1:
        return await duelnoplayer(ctx, challenger, game)
    try:
        challenged = await fetchu(ctx.message.raw_mentions[0])
    except IndexError:
        return await duelnoplayer(ctx, challenger, game)
    if challenger == challenged:
        # await ctx.send("You can't duel yourself!")
        # return 0
        pass
    if challenged.id == 811435588942692352 and game[0] == "C":
        return [challenger, challenged]
    message = await ctx.send(f"<@!{challenger.id}> has challenged <@!{challenged.id}> "
                             f"to a duel of **{game}**!  \n They have 30 seconds to confirm!")
    challenge_emojis = ["✅", "🚫"]
    for emoji in challenge_emojis:
        await message.add_reaction(emoji)

    def check(payload):
        return payload.message_id == message.id and str(payload.emoji) in challenge_emojis \
               and payload.user_id == challenged.id

    try:
        variable = await client.wait_for('raw_reaction_add', timeout=30.0, check=check)
        # print(variable.emoji)
        if str(variable.emoji) == "✅":
            #await ctx.send(f"The duel has begun! ✅")
            pass
        else:
            await ctx.send(f"The duel was denied! 🚫")
            return 0
    except asyncio.TimeoutError:
        await ctx.send(f"Uh Oh! {str(challenged)[:-5]} didn't respond in time!")
        return 0
    return [challenger, challenged]


async def duelnoplayer(ctx, challenger, game):
    message = await ctx.send(f"<@!{challenger.id}> is looking for a duel in **{game}**! \n"
                             f"There are 30 seconds left for someone to respond!")
    await message.add_reaction("✅")
    global accepted
    def check(payload):
        global accepted
        accepted = payload.user_id
        return payload.message_id == message.id and str(
            payload.emoji) == "✅" and not payload.user_id in {811435588942692352, challenger.id}

    try:
        await client.wait_for('raw_reaction_add', timeout=30.0, check=check)
        accepted = await fetchu(accepted)
        #await ctx.send(f"<@!{accepted.id}> accepted the challenge! ✅")
    except asyncio.TimeoutError:
        await ctx.send(f"Uh Oh! Nobody responded in time!")
        return 0
    return [challenger, accepted]