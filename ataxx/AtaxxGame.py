# Created by Lee, Jun Seok <lego3410@gmail.com> at Sep 6, 2020
import sys
sys.path.append('..')
from Game import Game
from .AtaxxLogic import Board, _directions_1, _directions_2
import numpy as np


action2move = []

for x in range(7):
  for y in range(7):
    action2move.append((None, None, x, y))

for x in range(7):
  for y in range(7):
    for dx, dy in _directions_2:
      if {x, y, x+dx, y+dy} <= set(range(7)):
        action2move.append((x, y, x+dx, y+dy))

action2move.append((None, None, None, None))

move2action = {e:i for i, e in enumerate(action2move)}


class AtaxxGame(Game):
  square_content = {
    -1: "X",
    +0: "-",
    +1: "O"
  }

  @staticmethod
  def getSquarePiece(piece):
    return AtaxxGame.square_content[piece]
  
  def __init__(self, n):
    pass
  
  def getInitBoard(self):
    b = Board()
    return np.array(b.pieces)
  
  def getBoardSize(self):
    return (7, 7)
  
  def getActionSize(self):
    # 49 for clone actions
    # 4 * (35 + 30 + 25 + 30) for move actions
    return 530

  def getNextState(self, board, player, action):
    # if player takes action on board, return next (baord, player)
    # action must be a valid move
    b = Board()
    b.pieces = np.copy(board)
    move = action2move[action]
    b.execute_move(move, player)
    return b.pieces, -player

  def getValidMoves(self, board, player):
    valids = [0]*self.getActionSize()
    b = Board()
    b.pieces = np.copy(board)
    legalMoves = b.get_legal_moves(player)
    if len(legalMoves) == 0:
      return np.array(valids)
    for x0, y0, x1, y1 in legalMoves:
      valids[move2action[x0, y0, x1, y1]] = 1
    return np.array(valids)

  def getGameEnded(self, board, player):
    # return 0 if not ended, 1 if given player won, -1 if given player lost
    b = Board()
    b.pieces = np.copy(board)
    if b.has_legal_moves(player):
      return 0
    if b.has_legal_moves(-player):
      return 0
    if b.countDiff(player) > 0:
      return 1
    return -1
  
  def getCanonicalForm(self, board, player):
    return player*board
  
  # TODO: implement symmetries
  # def getSymmetries(self, board, pi):
  #   assert(len(pi) == self.getActionSize())
  #   move2pi = {}
  #   for move, value in zip(action2move.values(), pi):
  #     move2pi[move] = value

  #   for i in range(1, 5):
  #     for j in [True, False]:
  #       newB = np.rot90(board, i)

  #       if j:
  #         newB = np.fliplr(newB)
        
  #       l += [(newB, list())]

  def stringRepresentation(self, board):
    return board.tostring()
  
  def stringRepresentationReadable(self, board):
    board_s = "".join(self.square_content[square] for row in board for square in row)
    return board_s
  
  def getScore(self, board, player):
    b = Board()
    b.pieces = np.copy(board)
    return b.countDiff(player)

  @staticmethod
  def display(board):
    n = board.shape[0]
    print("   ", end="")
    for y in range(n):
      print(y, end=" ")
    print("")
    print("-----------------------")
    for y in range(n):
      print(y, "|", end="")    # print the row #
      for x in range(n):
        piece = board[y][x]    # get the piece to print
        print(AtaxxGame.square_content[piece], end=" ")
      print("|")

    print("-----------------------")
