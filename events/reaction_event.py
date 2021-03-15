from gaming.rps import rpsgame
import gaming.tictactoe as ttt

async def check(payload, rpsgames, tttgames):
    await ttt.on_reaction(payload, tttgames)
    await rpsgame(payload, rpsgames)