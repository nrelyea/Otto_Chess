import chess
import pygame

from const import *
from square import Square
from piece import *

class DisplayBoard:

    def __init__(self):
        self.squares = [[0,0,0,0,0,0,0,0] for col in range(COLS)]

        self.flipped = False
        self.activeBoard = chess.Board()    # create default inital chess board

        self.flipButtonRect = (8 * SQSIZE + (SIDEBARBORDERSIZE * 2), 4 * SQSIZE - (SIDEBARSIZE - (SIDEBARBORDERSIZE * 4)) // 2, SIDEBARSIZE - (SIDEBARBORDERSIZE * 4), SIDEBARSIZE - (SIDEBARBORDERSIZE * 4))
        
        self._create()
        self._update_pieces()

    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)
       

    def _update_pieces(self):

        #print(self.activeBoard)

        # Clear previous squares state
        self._create()

        for squareNum in range(0,64):           
            if self.activeBoard.piece_at(squareNum) != None:
                piece = self.activeBoard.piece_at(squareNum)
                row = self._square_num_to_coords(squareNum)[0]
                col = self._square_num_to_coords(squareNum)[1]
                #print('piece found at ' + str(row) + ',' + str(col) + ': ' + str(piece))

                if(self.flipped):
                    row = 7 - row
                    col = 7 - col

                self.squares[row][col] = Square(row, col, self._piece_to_Obj(piece))
                
                

    # convert board piece to correct Class Obj
    def _piece_to_Obj(self, piece):
        match str(piece):
                    case 'P':
                        return Pawn('white')
                    case 'N':
                        return Knight('white')
                    case 'B':
                        return Bishop('white')
                    case 'R':
                        return Rook('white')
                    case 'Q':
                        return Queen('white')
                    case 'K':
                        return King('white')
                    case 'p':
                        return Pawn('black')
                    case 'n':
                        return Knight('black')
                    case 'b':
                        return Bishop('black')
                    case 'r':
                        return Rook('black')
                    case 'q':
                        return Queen('black')
                    case 'k':
                        return King('black')
    
    def _square_num_to_coords(self, num):
        row = int((num)/8)
        col = num - (8 * row)
        row = 7 - row
        return (row, col)

    def CoordsToSquareName(self, coords):
        row = coords[0]
        col = coords[1]
        letters = ['a','b','c','d','e','f','g','h']
        numbers = [1,2,3,4,5,6,7,8]
        return str(letters[col]) + str(numbers[7-row])

    def SquareNameToCoords(self, coords):
        pass

    def _update_sidebar(self, surface):
        borderRect = (8 * SQSIZE, 0, SIDEBARSIZE, 8 * SQSIZE)
        mainRect = (8 * SQSIZE + SIDEBARBORDERSIZE, SIDEBARBORDERSIZE, SIDEBARSIZE - (SIDEBARBORDERSIZE * 2), 8 * SQSIZE - (SIDEBARBORDERSIZE * 2))
               
        if self.activeBoard.turn == chess.WHITE:
            pygame.draw.rect(surface, (0,0,0), borderRect)
            pygame.draw.rect(surface, (255,255,255), mainRect)
        else:
            pygame.draw.rect(surface, (255,255,255), borderRect)
            pygame.draw.rect(surface, (0,0,0), mainRect)
        
        self._draw_Flip_Button(surface)
    
    def _draw_Flip_Button(self, surface):
        buttonColor = (130, 190, 245)
        buttonTextColor = (0,0,0)

        pygame.draw.rect(surface, buttonColor, self.flipButtonRect)

        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('Flip', True, buttonTextColor, buttonColor)
        textRect = text.get_rect()
        textRect.center = (8 * SQSIZE + (SIDEBARSIZE // 2), 4 * SQSIZE)
        surface.blit(text, textRect)
    
    def flip_board(self):
        self.flipped = not self.flipped
        print('Flipped? ' + str(self.flipped))

        self._update_pieces()
        pass



                    