async def checkreaction():
    if not payload.user_id == 811435588942692352:
        for game in games:
            await rpsgame(payload, game)