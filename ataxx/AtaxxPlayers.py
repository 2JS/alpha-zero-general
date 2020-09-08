from .AtaxxGame import move2action, action2move
import numpy as np


class RandomPlayer:
  def __init__(self, game):
    self.game = game

  def play(self, board):
    a = np.random.randint(self.game.getActionSize())
    valids = self.game.getValidMoves(board, 1)
    while valids[a]!=1:
      a = np.random.randint(self.game.getActionSize())
    return a


class HumanAtaxxPlayer:
  def __init__(self, game):
    self.game = game

  def play(self, board):
    # display(board)
    valid = self.game.getValidMoves(board, 1)
    for i in range(len(valid)):
      if valid[i]:
        print("(%s %s %s %s)" % action2move[i], end=" ")
    while True:
      input_move = input()
      input_a = input_move.split(" ")
      if len(input_a) == 4:
        try:
          a = tuple(map((lambda x: None if x == 'n' else int(x)), input_a))
          print(a)
          a = move2action[a]
          print(a)
          if valid[a]:
            break
        except ValueError:
          # Input needs to be an integer
          'Invalid integer'
        except KeyError:
          'Invalid move'
      print('Invalid move')
    return a


class GreedyAtaxxPlayer:
  def __init__(self, game):
    self.game = game

  def play(self, board):
    valids = self.game.getValidMoves(board, 1)
    candidates = []
    for a in range(self.game.getActionSize()):
      if valids[a]==0:
        continue
      nextBoard, _ = self.game.getNextState(board, 1, a)
      score = self.game.getScore(nextBoard, 1)
      candidates += [(-score, a)]
    candidates.sort()
    return candidates[0][1]
