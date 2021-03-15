class TictactoeBoard:
    def __init__(self, board="---------"):
        self.board_string = board
        self.whos_turn = "x"
        self.board_message = None
        self.text_message = None
        self.players = None
        self.turnIndex = 0

    def toOutputBoard(self):
        reactions = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]
        x = "❌"
        o = "⭕"
        board_string = self.board_string

        tempList = list(board_string)
        reactions_used = []
        for i in range(len(tempList)):
            if tempList[i] == "-":
                tempList[i] = reactions[i]
                reactions_used.append(reactions[i])
        tempList.insert(3, "\n")
        tempList.insert(7, "\n")
        formatted = "".join(tempList)
        formatted = formatted.replace("x", x)
        formatted = formatted.replace("o", o)
        return formatted, reactions_used
    def makeMove(self, who, index):
        tempList = list(self.board_string)
        tempList[index] = who
        self.board_string = "".join(tempList)
        self.turnIndex += 1
        self.whos_turn = "x" if self.whos_turn != "x" else "o"

    def buttonToIndex(self, buttonIndex):
        current_button = 0
        for i in range(len(self.board_string)):
            if self.board_string[i] == "-":
                if current_button == buttonIndex:
                    return i
                current_button+=1
    def checkForGame(self):
        b = self.board_string
        for i in ["x", "o"]:
            if b[:3] == i*3 or b[3:6] == i*3 or b[6:] == i*3:
                return [True, i]
            elif b[0]+b[3]+b[6] == i*3 or b[1]+b[4]+b[7] == i*3 or b[2]+b[5]+b[8] == i*3:
                return [True, i]
            elif b[0]+b[4]+b[8] == i*3 or b[2]+b[4]+b[6] == i*3:
                return [True, i]
            elif b.count("-") == 0:
                return [True, "Tie"]
        return [False,]