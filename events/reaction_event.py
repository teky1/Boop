from gaming.rps import rpsgame

async def check(payload, rpsgames):
    await rpsgame(payload, rpsgames)