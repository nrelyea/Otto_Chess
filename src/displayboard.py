import chess

from const import *
from square import Square
from piece import *

class DisplayBoard:

    def __init__(self):
        self.squares = [[0,0,0,0,0,0,0,0] for col in range(COLS)]

        self.activeBoard = chess.Board()
        #print(self.activeBoard)

        self._create()
        self._update_pieces()



    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

    def _update_pieces(self):
        for squareNum in range(0,64):           
            if self.activeBoard.piece_at(squareNum) != None:
                piece = self.activeBoard.piece_at(squareNum)
                row = self._square_num_to_coords(squareNum)[0]
                col = self._square_num_to_coords(squareNum)[1]
                #print('piece found at ' + str(row) + ',' + str(col))
                match str(piece):
                    case 'P':
                        self.squares[row][col] = Square(row, col, Pawn('white'))
                    case 'N':
                        self.squares[row][col] = Square(row, col, Knight('white'))
                    case 'B':
                        self.squares[row][col] = Square(row, col, Bishop('white'))
                    case 'R':
                        self.squares[row][col] = Square(row, col, Rook('white'))
                    case 'Q':
                        self.squares[row][col] = Square(row, col, Queen('white'))
                    case 'K':
                        self.squares[row][col] = Square(row, col, King('white'))
                    case 'p':
                        self.squares[row][col] = Square(row, col, Pawn('black'))
                    case 'n':
                        self.squares[row][col] = Square(row, col, Knight('black'))
                    case 'b':
                        self.squares[row][col] = Square(row, col, Bishop('black'))
                    case 'r':
                        self.squares[row][col] = Square(row, col, Rook('black'))
                    case 'q':
                        self.squares[row][col] = Square(row, col, Queen('black'))
                    case 'k':
                        self.squares[row][col] = Square(row, col, King('black'))
    
    def _square_num_to_coords(self, num):
        row = int((num)/8)
        col = num - (8 * row)
        row = 7 - row
        return (row, col)

                    