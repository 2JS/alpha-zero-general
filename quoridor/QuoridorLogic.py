# Created by Lee, Jun Seok <lego3410@gmail.com> at Sep 17, 2020
import numpy as np

__moves = [(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1)]
# move format
# moving moves (8)
# put vwalls (64)
# put hwalls (64)
# total (136)

class Board:
  def __init__(self):
     # (x, y, # of walls). player 1 first, player -1 second.
    self.players = [(4, 0, 10), (4, 8, 10)]
    # +1: vertical walls
    # +0: no walls 
    # -1: horizontal walls
    self.walls = np.zeros((8,8), type=int)
  
  def __getitem__(self, index):
    return self.pieces[index]
  
  def get_legal_actions(self, color):
    # returns list of 136 [0, 1], valid moves
    x, y, _ = self.p[color]
    actions = [0 for _ in range(140)]

    # move actions
    for dx, dy in __moves:
      if abs(dx) + abs(dy) == 1: # regular move
        pass
      elif dx*dy == 0: # straight jump
        pass
      else: # diagonal jump
        pass
    
    # wall actions
    
  def get_board(self, player=1):
    b = np.zeros((17,17))
    # performance issue may occur
    vwalls = np.vectorize((lambda x: max(x, 0)))(self.walls)
    hwalls = np.vectorize((lambda x: max(-x, 0)))(self.walls)

    b[:-1:2, 1::2] = vwalls
    b[2::2, 1::2] += vwalls

    b[1::2, :-1:2] = hwalls
    b[1::2, 2::2] += hwalls

    b[::2, 1::2] = np.vectorize((lambda x: min(x, 1)))(b[::2, 1::2])
    b[1::2, ::2] = np.vectorize((lambda x: min(x, 1)))(b[1::2, ::2])

    x0, y0, _ = self.players[0]
    x1, y1, _ = self.players[1]
    
    b[2*x0, 2*y0] = 1
    b[2*x1, 2*y1] = -1

    return b


  def execute_move(self, move, color):
    pass
