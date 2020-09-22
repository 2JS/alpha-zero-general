import sys
sys.path.append('..')
from Game import Game
from .QuoridorLogic import Board
import numpy as np


class QuoridorGame(Game):
  def __init__(self):
    pass

  def getInitBoard(self):
    b = Board()
    return np.array(b.pieces)

  def getBoardSize(self):
    return 17, 17

  def getActionSize(self):
    return 12
  
  def getNextState(self, board, player, action):
    pass

  def getValidMovew(self, board, player):
    pass

  def getGameEnded(self, board, player):
    b = Board()
    b.pieces = np.copy(board)
    
    for x in range(0, 17, 2):
      if b.pieces[0][x] == -1:
        return -player
    
    for x in range(0, 17, 2):
      if b.pieces[16][x] == 1:
        return player
    
    return 0
  
  def getCanonicalForm(self, board, player):
    return player*board
  
  def getSymmetries(self, board, pi):
    # don't need rotations. only flip
    pass

  @staticmethod
  def display(board):
    square_content = {
      -1: "X",
      +0: " ",
      +1: "O"
    }
    print("   ", end="")
    for y in range(9):
      print(y, end=" ")
    print("\n--+-+-+-+-+-+-+-+-+-+->x")
    for y in range(9):
      print(y, "|", end="")
      for x in range(9):
        piece = board[y][x]
        
        print(square_content[piece], end=)
      