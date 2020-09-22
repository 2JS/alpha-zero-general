# Created by Lee, Jun Seok <lego3410@gmail.com> at Sep 17, 2020

__moves = [(0,2),(0,1),(1,1),(2,0),(1,0),(1,-1),(0,-2),(0,-1),(-1,-1),(-2,0),(-1,0),(-1,1)]
# move format
# moving moves (12)
# put vwalls (64)
# put hwalls (64)
# total (140)

class Board:
  def __init__(self):
    self.p = {1:(4, 8, 10), -1:(4, 0, 10)} # x, y, # of walls of p1, p-1
    self.pieces = [[0 for _ in range(17)] for _ in range(17)]
  
  def __getitem__(self, index):
    return self.pieces[index]
  
  def get_legal_actions(self, color):
    # returns list of 140 [0, 1], valid moves
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
    


  def execute_move(self, move, color):
    pass
