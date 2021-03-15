import random
import gaming.gamestart as gamestart
from objects.tttboard_obj import TictactoeBoard

reactions = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]

async def _tictactoe(ctx, client, games):
    players = await gamestart.duelstart(ctx, "Tic Tac Toe", client)

    if players == 0:
        return

    board_str = "---------"
    board = TictactoeBoard(board_str)
    random.shuffle(players)
    board.players = players
    output_string, reactions_used = board.toOutputBoard()

    current_player_turn = board.players[board.turnIndex % 2]

    board.board_message = await ctx.send(output_string)
    board.text_message = await ctx.send(
        f"<@!{current_player_turn.id}>, you go first! Choose a square through the reaction")

    games.games.append(board)
    for i in reactions_used:
        await board.board_message.add_reaction(i)


async def on_reaction(payload, games):
    for i in range(len(games.games)):
        if games.games[i].board_message.id == payload.message_id and payload.member.bot is False:
            board = games.games[i]
            current_player_turn = board.players[board.turnIndex % 2]
            brd, reactions_available = board.toOutputBoard()
            if payload.user_id != current_player_turn.id or str(payload.emoji) not in reactions_available:
                return
            buttonIndex = reactions.index(str(payload.emoji))
            board.makeMove(board.whos_turn, buttonIndex)
            new_board, reactions_used = board.toOutputBoard()
            results = board.checkForGame()
            symbols = ["❌", "⭕"]
            if results[0]:
                if results[1] == "Tie":
                    msg = f"<@!{board.players[0].id}> {symbols[0]} and <@!{board.players[1].id}> {symbols[1]} have tied!!"
                elif results[1] == "x":
                    msg = f"<@!{board.players[0].id}> {symbols[0]} has *destroyed* <@!{board.players[1].id}> {symbols[1]} in this respectable game of TICTACTOE!!!!"
                elif results[1] == "o":
                    msg = f"<@!{board.players[1].id}> {symbols[1]} has *destroyed* <@!{board.players[0].id}> {symbols[0]} in this respectable game of TICTACTOE!!!!"

                await board.board_message.clear_reactions()
                await board.board_message.edit(content=new_board)
                await board.text_message.edit(content=msg)
                return

            current_player_turn = board.players[board.turnIndex % 2]
            current_symbol = symbols[board.turnIndex % 2]

            await board.board_message.clear_reaction(payload.emoji)
            await board.board_message.edit(content=new_board)
            await board.text_message.edit(content=f"<@!{current_player_turn.id}> it is now your turn! You are {current_symbol} Choose a square through the reaction. ({board.turnIndex})")