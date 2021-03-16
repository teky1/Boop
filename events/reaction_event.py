from gaming.rps import rpsgame
import gaming.tictactoe as ttt
from gaming.connectfour import connectevent

async def check(payload, rpsgames, tttgames, c4games, client):
    await ttt.on_reaction(payload, tttgames)
    await rpsgame(payload, rpsgames)
    await connectevent(payload, c4games, client)