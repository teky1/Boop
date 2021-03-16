import random
from objects.c4_obj import ConnectGame
from gaming.gamestart import duelstart
import json

usercache = {}  # TEKY IM SORRY I NEEDED FETCHM AND FETCHU I DONT WANNA GO BACK TO BEING SLOW
messagecache = {}


async def connectevent(payload, c4games, client):
    for c4game in range(len(c4games.games)):
        # c4 = rehydrate(c4games[-1 - c4game])
        c4 = rehydrate(c4games.games[-1 - c4game])
        done = await fourconnect(payload, c4, -1 - c4game, c4games, client)
        if done is not None:
            break


async def _connect4(ctx, issmall, c4games, client):
    output = await alterc4inputs(ctx)
    if output == None:
        return
    rows = output[0]
    columns = output[1]
    note = output[2]
    result = await duelstart(ctx, f"Connect 4 ({columns}x{rows})", client)
    if result == 0:
        return
    if random.randint(0, 1) == 0:
        p1 = result[0]
        p2 = result[1]
    else:
        p1 = result[1]
        p2 = result[0]
    player1 = str(p1)[:-5]
    player2 = str(p2)[:-5]

    c4game = ConnectGame(rows, columns, p1.id, p2.id)  # THE GAME IS CREATED HEREEEEEEEEEEE
    c4game.issmall = issmall

    await ctx.send(f"{note}The game has begun! P1: {player1} 🔴, P2: {player2} 🔵")
    rowsleft = rows
    while rowsleft > 0:
        tempmessage = await ctx.send(c4game.formatrow(rowsleft))
        c4game.messages[1].append(tempmessage.id)
        if 3 >= rowsleft >= 1:
            c4game.leftovers = rowsleft
        rowsleft -= 3
    c4game.messages[2] = tempmessage.id
    c4game.messages[0] = tempmessage.channel.id
    c4game.messages[3] = await ctx.send(f"{player1} goes first!")
    c4game.messages[3] = c4game.messages[3].id
    c4game.messages[1].reverse()
    # [[rowchannelid], [rowids], [reactorid], [infoid]]

    emojis = ["✅", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]
    for emoji in range(columns+1):
        await tempmessage.add_reaction(emojis[emoji])

    if p1.id == 811435588942692352:
        c4game.simpleai()
        c4game.new = False
        c4game.array[c4game.y][c4game.x] = 1
        rowid = round((c4game.y - c4game.leftovers) / 3 - .4)
        if rowid < 0:
            rowid = -1
        j = await fetchm(c4game.messages[0], c4game.messages[1][rowid + 1], client)
        await j.edit(content=c4game.formatrow(c4game.leftovers + 3 * (rowid + 1)))
        if c4game.turn:
            c4game.turn = 0
        else:
            c4game.turn = 1

    c4games.games.append(c4game.jsonify())
    with open("data/c4games.json", "w") as out_file:
        json.dump(c4games.games, out_file, indent=4)


async def fourconnect(payload, c4, index, c4games, client):
    c4emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]  # ✅
# c4.messages = [[channelid], [rowids], [reactorid], [infomessageid]]
#    if client.is_ws_ratelimited():
#        print("lag!")
    chid = c4.messages[0]
    if payload.message_id in c4.messages[1]:
        if payload.message_id == c4.messages[2]:
            if payload.user_id == c4.players[c4.turn]:
                k = await fetchm(chid, c4.messages[3], client)
                if str(payload.emoji) in c4emojis:
                    await k.edit(content=f"{await fetchu(payload.user_id, client)} selected {payload.emoji}. Check to confirm.")
                    await updatec4(c4, payload, index, 3, c4games, client)

                elif str(payload.emoji) == "✅" and c4.new:
                    c4.tops[c4.x] = c4.y+1
                    await updatec4(c4, payload, index, 1+c4.turn, c4games, client)
                    c4.new = False
                    if c4.checkforwin():
                        await k.edit(content=f"GAME OVER. {str(await fetchu(c4.players[c4.turn], client))} won!!!")

                        del c4games.games[index]
                        with open("data/c4games.json", "w") as out_file:
                            json.dump(c4games.games, out_file, indent=4)
                        return True
                    if c4.turn:
                        c4.turn = 0
                    else:
                        c4.turn = 1
                    botinfo = ""
                    if c4.players[c4.turn] == 811435588942692352:
                        # c4.doublefutureai()
                        # botdata = c4.recurseai()  # (self, fops, tarray, startturn, depth=3, passdown=[]
                        c4.simpleai()
                        # botinfo = f"(bard chose {botdata[0]+1} with confidence {botdata[1]}"
                        c4.new = False
                        c4.array[c4.y][c4.x] = c4.turn+1
                        rowid = round((c4.y - c4.leftovers) / 3 - .4)
                        if rowid < 0:
                            rowid = -1
                        j = await fetchm(c4.messages[0], c4.messages[1][rowid + 1], client)
                        await j.edit(content=c4.formatrow(c4.leftovers + 3 * (rowid + 1)))
                        if c4.checkforwin():
                            await k.edit(content=f"GAME OVER. {str(await fetchu(811435588942692352, client))} won!!!")
                            del c4games.games[index]
                            with open("data/c4games.json", "w") as out_file:
                                json.dump(c4games.games, out_file, indent=4)
                            return True
                        if c4.turn:
                            c4.turn = 0
                        else:
                            c4.turn = 1

                    await k.edit(content=f"It is now {str(await fetchu(c4.players[c4.turn], client))}'s turn. {botinfo}")

                    c4games.games[index] = c4.jsonify()
                    with open("data/c4games.json", "w") as out_file:
                        json.dump(c4games.games, out_file, indent=4)
            if not payload.user_id == 811435588942692352:
                h = await fetchm(chid, c4.messages[2], client)
                await h.remove_reaction(payload.emoji, await fetchu(payload.user_id, client))
        else:
            i = await fetchm(chid, payload.message_id, client)
            await i.remove_reaction(payload.emoji, await fetchu(payload.user_id, client))
        return True
    # game_messages = [[ctx, p1, p2, "c4", message, infomessage], x, y, turn, thegame, tops, new, rowids, rows]


async def updatec4(c4, payload, index, piece, c4games, client):
    c4emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]
    chid = c4.messages[0]
    k = await fetchm(chid, c4.messages[3], client)

    orowid = round((c4.y - c4.leftovers) / 3 - .4)
    if orowid < 0:
        orowid = -1
    if c4.array[c4.y][c4.x] == 3:
        c4.array[c4.y][c4.x] = 0
    if piece == 3:
        c4.x = c4emojis.index(str(payload.emoji))
        c4.y = c4.tops[c4.x]
    if not c4.y == c4.rows:
        c4.new = True
        c4.array[c4.y][c4.x] = piece
        rowid = round((c4.y - c4.leftovers) / 3 - .4)
        if rowid < 0:
            rowid = -1
        if not orowid == rowid:
            j = await fetchm(chid, c4.messages[1][orowid + 1], client)
            await j.edit(content=c4.formatrow(c4.leftovers + 3 * (orowid + 1)))
        j = await fetchm(chid, c4.messages[1][rowid + 1], client)
        await j.edit(content=c4.formatrow(c4.leftovers + 3 * (rowid + 1)))
        c4games.games[index] = (c4.jsonify())
    else:
        await k.edit(content=f"Invalid move; {str(await fetchu(c4.players[c4.turn], client))} must select again. (too high)")
        c4.new = False


async def alterc4inputs(ctx):
    note = ""
    splitted = ctx.message.content.split()
    if len(splitted) > 1:
        ignorelol = splitted[1]
    else:
        ignorelol = ""
    if len(splitted) == 4:
        columns = splitted[2]
        rows = splitted[3]
    elif len(splitted) <= 2:
        columns = 7
        rows = 6
    elif len(splitted) > 4:
        await ctx.send("...what\nb!c4 <mention someone (or leave empty)> <length> <height>")
        return
    elif len(splitted) == 3:
        columns = splitted[2]
        rows = 6
    else:
        await ctx.send("...what\nb!c4 <mention someone (or leave empty)> <length> <height>")
        return

    if str(columns).isdigit() and str(rows).isdigit():
        columns = int(columns)
        rows = int(rows)
    else:
        await ctx.send("...what\nb!c4 <mention someone (or leave empty)> <length> <height>")
        return
    try:
        ignorelol = int(ignorelol)
        if len(splitted) == 3 and type(columns) is int:
            rows = columns
            columns = ignorelol
        elif len(splitted) == 2:
            columns = ignorelol
    except ValueError:
        pass

    else:
        ignorelol = ""
    if columns < 4:
        columns = 4
        note = "4 is the minimum number of rows/columns\n"
    elif columns > 9:
        columns = 9
        note = "9 is the maximum number of columns\n"
    if rows < 4:
        rows = 4
        note = "4 is the minimum number of rows/columns\n"
    elif rows > 30:
        rows = 30
        note = "30 is the maximum number of rows\n"
    return [rows, columns, note]


def rehydrate(c4game):
    c4 = ConnectGame(c4game[0], c4game[1], c4game[2][0], c4game[2][1])
    c4.x = c4game[3]
    c4.y = c4game[4]
    c4.turn = c4game[5]
    c4.tops = c4game[6]
    c4.leftovers = c4game[7]
    c4.new = c4game[8]
    c4.messages = c4game[9]
    c4.array = c4game[10]
    c4.won = c4game[11]
    c4.issmall = c4game[12]
# [self.rows, self.columns, self.players, self.x, self.y, self.turn, self.tops, self.leftovers, self.new, self.messages, self.array]
    return c4


async def fetchm(channelid, messageid, client):  # THEY'RE JUST TOO GOODKJASBSJMSHBGSHGJ
    if str(messageid) in messagecache.keys():
        # print("old message")
        return messagecache[str(messageid)]
    else:
        # print("new message")
        thechannel = await client.fetch_channel(channelid)
        themessage = await thechannel.fetch_message(messageid)
        messagecache[str(messageid)] = themessage
    return themessage


async def fetchu(userid, client):  # SO YUMMYYYYYYYYYY
    if str(userid) in usercache.keys():
        # print("old user")
        return usercache[str(userid)]
    else:
        # print("new user")
        theuser = await client.fetch_user(userid)
        usercache[str(userid)] = theuser
    return theuser