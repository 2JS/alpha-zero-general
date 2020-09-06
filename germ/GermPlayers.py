import numpy as np
from .GermLogic import dict

class RandomPlayer:
    def __init__(self, game):
        self.game = game

    def play(self, board):
        a = np.random.randint(self.game.getActionSize())
        valids = self.game.getValidMoves(board, 1)
        while valids[a] != 1:
            a = np.random.randint(self.game.getActionSize())
        return a


class HumanOthelloPlayer:
    def __init__(self, game):
        self.game = game

    def play(self, board):
        # display(board)
        valid = self.game.getValidMoves(board, 1)
        for i in range(len(valid)):
            if valid[i]:
                print("[", int(i/self.game.n), int(i % self.game.n), end="] ")
        while True:
            input_move = input()
            input_a = input_move.split(" ")
            if len(input_a) == 4:
                try:
                    x0, y0, x1, y1 = [int(i) for i in input_a]
                    for key, value in dict.items():
                        if value == ((x1, y1), (x0-x1, y0-y1)):
                            if valid[key] == 1:
                                return key

                except ValueError:
                    # Input needs to be an integer
                    'Invalid integer'
            print('Invalid move')


class GreedyOthelloPlayer:
    def __init__(self, game):
        self.game = game

    def play(self, board):
        valids = self.game.getValidMoves(board, 1)
        candidates = []
        for a in range(self.game.getActionSize()):
            if valids[a] == 0:
                continue
            nextBoard, _ = self.game.getNextState(board, 1, a)
            score = self.game.getScore(nextBoard, 1)
            candidates += [(-score, a)]
        candidates.sort()
        return candidates[0][1]
