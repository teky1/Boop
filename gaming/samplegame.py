from gaming.gamestart import duelstart


async def _game(ctx, game, client):
    combatants = await duelstart(ctx, game, client)
    await ctx.send(combatants)