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
                    return [3, 3, 3, 3]
                return True
        if ai:
            return distances
        return False

    def jsonify(self):
        return [self.rows, self.columns, self.players, self.x, self.y, self.turn, self.tops, self.leftovers, self.new, self.messages, self.array, self.won, self.issmall]

    def boardscorer(self, turn=-1, ftops=None): #make it check the other player's best move, and both player's board's scores after this move
        boardscores = []
        for each in range(self.columns):
            x = each
            if ftops is None:
                y = self.tops[x]
            else:
                y = ftops[x]
            if y == self.rows:
                if ftops is None:
                    # print("HIGH!")
                    boardscores.append(-100)
                else:
                    boardscores.append(-5)
            else:
                if turn >= 0:
                    returned = self.checkforwin(True, x, y, turn)
                else:
                    returned = self.checkforwin(True, x, y)
                boardscores.append(returned[0] + returned[1] + returned[2]*1.2 + returned[3]*1.2)
        return boardscores

    def simpleai(self, forfuture=False, ftops=None, forsum=False):  # greedy algorithm doesnt see future

        board0 = self.boardscorer(0, ftops)
        board1 = self.boardscorer(1, ftops)
        centerbias = []
        sum = []

        for column in range(round(self.columns/2)):
            centerbias.append(round(0+0.1*column, 1))
        mid = centerbias[-1]
        if self.columns % 2 == 0:
            for column in range(round(self.columns/2)):
                centerbias.append(round(mid - 0.1*column, 1))
        else:
            for column in range(round(self.columns/2 - 0.1)):
                centerbias.append(round(mid - 0.1*(column+1), 1))

        for column in range(self.columns):
            if self.turn == 0:
                sum.append(board0[column] + board1[column]*0.5)
            if self.turn == 1:
                sum.append(board0[column]*0.5 + board1[column])
            sum[column] += centerbias[column]

        # print(f"p1: {board0}\np2: {board1}\nsum:{sum}")

        if forfuture:
            board0sum = 0
            board1sum = 0
            for item in board0:
                board0sum += item
            for item in board1:
                board1sum += item
            return [board0sum, board1sum]
        elif forsum:
            return sum
        else:
            bestscore = 0
            bestmoves = []
            for column in sum:
                if column > bestscore:
                    bestmoves = [sum.index(column)]
                    bestscore = column
                elif column == bestscore:
                    bestmoves.append(sum.index(column))
            bestmove = bestmoves[random.randint(0, len(bestmoves) - 1)]
            self.x = bestmove
            self.y = self.tops[self.x]
            self.tops[self.x] += 1
            self.array[self.y][self.x] = self.turn + 1
            return bestmove
