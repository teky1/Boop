import random

class C4games:
    def __init__(self):
        self.games = []
        self.startingturn = [0, 1]

    def newstart(self):
        if random.randint(0, 3) is True:
            self.startingturn.reverse()
        return self.startingturn
