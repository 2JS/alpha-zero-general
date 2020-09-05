'''
Author: Eric P. Nichols
Date: Feb 8, 2008.
Board class.
Board data:
  1=white, -1=black, 0=empty
  first dim is column , 2nd is row:
     pieces[1][7] is the square in column 2,
     at the opposite end of the board in row 8.
Squares are stored and manipulated as (x,y) tuples.
x is the column, y is the row.
'''

dict = {}

i = 0

for dx, dy in [(0, 0), (0, 2), (1, 2), (2, 2), (2, 1), (2, 0), (2, -1), (2, -2), (1, -2), (0, -2), (-1, -2), (-2, -2), (-2, -1), (-2, 0), (-2, 1), (-2, 2), (-1, 2)]:
    for x in range(7):
        for y in range(7):
            if 0 <= x + dx < 7 and 0 <= y + dy < 7:
                dict[i] = (x + dx, y + dy), (-dx, -dy)
                i += 1

dict[529] = (None, None), (None, None)


class Board:

    # list of all 8 directions on the board, as (x,y) offsets

    def __init__(self, n):
        "Set up initial board configuration."

        self.n = n
        # Create the empty board array.
        self.pieces = [None]*self.n
        for i in range(self.n):
            self.pieces[i] = [0]*self.n

        # sic
        # Set up the initial 4 pieces.
        self.pieces[int(self.n)-1][0] = 1
        self.pieces[0][int(self.n)-1] = 1
        self.pieces[0][0] = -1
        self.pieces[int(self.n)-1][int(self.n)-1] = -1

    # add [][] indexer syntax to the Board
    def __getitem__(self, index):
        return self.pieces[index]

    def countDiff(self, color):
        """Counts the # pieces of the given color
        (1 for white, -1 for black, 0 for empty spaces)"""
        count = 0
        for y in range(self.n):
            for x in range(self.n):
                if self[x][y] == color:
                    count += 1
                if self[x][y] == -color:
                    count -= 1
        return count

    # sic
    def get_legal_moves(self, color):
        """Returns all the legal moves for the given color.
        (1 for white, -1 for black
        """
        moves = set()  # stores the legal moves.

        for key, ((x, y), (dx, dy)) in dict.items():
            if key == len(dict) - 1:
                continue
            elif dx == 0 and dy == 0:
                if self[x][y] == 0 and color in [self[x][y] for x, y in [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]]:
                    moves.add(key)
            else:
                if self[x][y] == 0 and self[x+dx][y+dy] == color:
                    moves.add(key)

        return list(moves)

    def has_legal_moves(self, color):
        return len(self.get_legal_moves(color)) > 0

    # sic
    def execute_move(self, move, color):
        """Perform the given move on the board; flips pieces as necessary.
        color gives the color pf the piece to play (1=white,-1=black)
        """

        #Much like move generation, start at the new piece's square and
        #follow it on all 8 directions to look for a piece allowing flipping.

        # Add the piece to the empty square.
        # print(move)

        (x, y), (dx, dy) = move

        assert self[x][y] == 0
        assert self[x+dx][y+dy] == (color if not (dx == 0 and dy == 0) else 0)

        flips = self._get_flips(move, color)

        for x, y in flips:
            self[x][y] = color

        if not (dx == 0 and dy == 0):
            self[x+dx][y+dy] = 0
        self[x][y] = color

    def _get_flips(self, move, color):
        """ Gets the list of flips for a vertex and direction to use with the
        execute_move function """
        #initialize variables
        (x, y), (dx, dy) = move
        flips = []

        for (a, b) in [(x - 1, y), (x - 1, y - 1), (x - 1, y + 1), (x, y - 1), (x, y + 1), (x + 1, y), (x + 1, y - 1)]:
            if 0 <= a < 7 and 0 <= b < 7:
                if self[x][y] == -color:
                    flips.append((a, b))

        return flips

