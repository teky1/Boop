import random

class ConnectGame:

    def __init__(self, rows, columns, p1, p2):
        self.array = [[0 for i in range(columns)] for j in range(rows)]
        self.rows = rows
        self.columns = columns
        self.players = [p1, p2]
        self.x = 0
        self.y = 0
        self.turn = 0
        self.tops = [0] * columns
        self.leftovers = 0
        self.new = False
        self.messages = [[], [], [], []]
        self.won = False
        self.issmall = False
        # [[rowchannelid], [rowids], [reactorchannelid reactorid], [infochannelid, infoid]]

    def formatrow(self, rowsleft):
        if self.issmall:
            message2 = str(self.array[::-1])[1:-1]
            message2 = message2.replace("[", "| ").replace("]", " |\n").replace(" ", "").replace(",", "")
            themessage = message2.replace("0", "🔳 ").replace("1", "🔴 ").replace("2", "🔵 ").replace("3", "❔ ")
            themessage = themessage.replace("|", "| ")
        else:
            message = str(self.array)[2:-2]
            message = message.replace(" ", "").replace(",", "").split("][")
            #print(message)
            if rowsleft >= 3:
                upperrow = rowsleft-1
                lowerrow = upperrow-2
            else:
                upperrow = rowsleft-1
                lowerrow = 0
            themessage = " "
            for bruh in range(upperrow-lowerrow+1):
                if self.issmall:
                    themessage = "| "+message[lowerrow+bruh]+"|"+themessage
                else:
                    themessage = message[lowerrow+bruh]+themessage
                if not bruh == upperrow-lowerrow:
                    themessage = "\n" + themessage
            themessage = themessage.replace("0", "🔳 ").replace("1", "🔴 ").replace("2", "🔵 ").replace("3", "❔ ")

        return themessage

    def jsonify(self):
        return [self.rows, self.columns, self.players, self.x, self.y, self.turn, self.tops, self.leftovers, self.new, self.messages, self.array, self.won, self.issmall]

    def nothr33zz(self):
        for cleary in range(self.rows):
            for clearx in range(self.columns):
                if self.array[cleary][clearx] == 3:
                    self.array[cleary][clearx] = 0

    def checkforwin(self, ai=False, x=0, y=0, turn=0):
        directions = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, -1], [1, -1], [-1, 1]]  # -> <- | | / / \ \
        distances = [0, 0, 0, 0]  # - | / \
        for direction in directions:
            try:
                for distance in range(3):
                    if ai:
                        newy = y + (distance + 1) * direction[1]
                        newx = x + (distance + 1) * direction[0]
                    else:
                        newy = self.y+(distance+1)*direction[1]
                        newx = self.x+(distance+1)*direction[0]
                    if newx >= 0 and newy >= 0:
                        if ai:
                            if self.array[newy][newx] == turn+1:
                                distances[round(directions.index(direction)/2-.1)] += 1
                            elif ai and self.array[newy][newx] == 0:
                                pass
                            else:
                                break
                        else:
                            if self.array[newy][newx] == self.turn+1:
                                distances[round(directions.index(direction)/2-.1)] += 1
                            elif ai and self.array[newy][newx] == 0:
                                pass
                            else:
                                break
                    else:
                        break
            except IndexError:
                # print(f"indexerror at direction {direction}")
                pass
            if 3 in distances or 4 in distances or 5 in distances or 6 in distances:
                if ai:
                    return [69]
                else:
                    return True
            # elif 2 in distances:
            #     if ai:
            #         return[420]
        if ai:
            return distances
        return False

    def c4ai(self):
        directions = [[1, 0], [-1, 0], [1, 1], [-1, -1], [1, -1], [-1, 1], [0, -1], [0, 1]]  # -> <- / / \ \ |
        strat = [[0 for i in range(self.columns)] for j in range(self.rows)]
        boardscores = []
        enemyscores = []
        if self.turn == 0:
            first = 2
            second = 1
        else:
            first = 1
            second = 2
        # count - /  \ |  # 0 = nothing, 1 = tops, 2 = forbidden, 3 = p1 wins, 4 = p2 wins
        for x in range(self.columns):
            for y in range(self.rows):
                y = self.rows-y-1
                if self.tops[x] == self.rows:  # if topped out
                    boardscores.append(-250)
                    enemyscores.append(-250)
                    break
                if not self.array[y][x] == 0:
                    break
                else:  # check every whitespace for a three in a row, and mark them
                    for turnpiece in [first, second]:
                        # print(f"{turnpiece}, ({x+1}, {y+1})")
                        distances = [0, 0, 0, 0]
                        raylength = [0, 0, 0, 0]
                        realscore = [0, 0, 0, 0]
                        inarow = [0, 0, 0, 0]

                        for direction in directions:
                            space = False
                            axis = round(directions.index(direction) / 2 - .1)
                            try:
                                for distance in range(3):
                                    newy = y + (distance + 1) * direction[1]
                                    newx = x + (distance + 1) * direction[0]
                                    if not self.columns > newx >= 0 or not self.rows > newy >= 0:
                                        break
                                    if self.array[newy][newx] == turnpiece:
                                        distances[axis] += 1
                                        raylength[axis] += 1
                                        if space is False:
                                            inarow[axis] += 1
                                            if inarow[axis] >= 3:
                                                # print(f"{turnpiece}, ({x + 1}, {y + 1})")
                                                # print(f"WINNING BOARD: {self.array}")
                                                # print(f"CONSECUTIVE DIRECTION SCORES: {inarow}")
                                                if strat[y][x] != 2:
                                                    strat[y][x] = turnpiece + 2
                                                if y > 0:
                                                    strat[y-1][x] = 2
                                                space = True

                                    elif self.array[newy][newx] == 0:
                                        raylength[axis] += 1
                                        space = True

                                    else:
                                        break  # opponent piece or glitch 3

                            except IndexError:
                                pass

                            if raylength[axis] >= 3:
                                realscore[axis] = 1.5*distances[axis]**2+0.5  # add biases later
                            elif raylength[axis] == 2:
                                realscore[axis] = 0.5*distances[axis]**2
                            elif raylength[axis] == 1:
                                realscore[axis] = 0.2*distances[axis]**2
                        if turnpiece == self.turn+1 and y == self.tops[x]:  # turnpiece == self.turn+1 and
                            if strat[y][x] == 2:
                                if strat[y+1][x] == turnpiece+2 and strat[y+2][x] == turnpiece+2:
                                    boardscores.append(60)
                                else:
                                    boardscores.append(-100)
                            elif strat[y][x] == 0:
                                boardscores.append(realscore[0] + realscore[1]*1.2 + realscore[2]*1.2 + realscore[3]*0.6)
                            elif strat[y][x] + self.turn == 4:  # 4 and 0, or 1 and 3
                                boardscores.append(100)
                            else:
                                boardscores.append(200)
                            # print(raylength)
                            # print(distances)
                            # print(realscore)
                            # print(f"({x+1}, {y+1}) is {strat[y][x]}, so {boardscores[-1]}")
                        elif y == self.tops[x]:
                            if strat[y][x] == 2:
                                if strat[y+1][x] == turnpiece+2:
                                    enemyscores.append(-120)
                                else:
                                    enemyscores.append(60)
                            elif strat[y][x] == 0:
                                enemyscores.append(realscore[0] + realscore[1]*1.2 + realscore[2]*1.2 + realscore[3]*0.6)
                            elif strat[y][x] + self.turn == 4:
                                enemyscores.append(100)
                            else:
                                enemyscores.append(200)
                            # print(raylength)
                            # print(distances)
                            # print(realscore)
                            # print(f"({x+1}, {y+1}) is {strat[y][x]}, so {enemyscores[-1]}")

        centerbias = []
        for column in range(round(self.columns/2+.1)):
            centerbias.append(0+0.01*column)
        # print("uhh", centerbias)
        mid = centerbias[-1]
        if self.columns % 2 == 0:
            for column in range(round(self.columns/2)):
                centerbias.append(mid - 0.01*column)
        else:
            for column in range(round(self.columns/2 - 0.1)):
                centerbias.append(mid - 0.01*(column+1))

        for index in range(self.columns):
            try:
                yourscore = boardscores[index]*100
                centerscore = centerbias[index]*100
                enemyscore = enemyscores[index]*70
                boardscores[index] = round(yourscore + centerscore + enemyscore)
            except IndexError:
                print(boardscores)
                print(enemyscores)
                print(centerbias)
            # boardscores[index] = round((boardscores[index]+centerbias[index])*100 + enemyscores[index]*70)

        bestmove = boardscores.index(max(boardscores))

        # print(str(strat[::-1]).replace("], [", ",\n")[2:-2])
        # print(boardscores)

        # bestmove = random.randint(0, 6)
        self.x = bestmove
        self.y = self.tops[self.x]
        self.tops[self.x] += 1
        self.array[self.y][self.x] = self.turn + 1