from socket import gaierror
import pygame
import sys
import chess


from const import *
from game import Game

class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
        pygame.display.set_caption('Chess')
        self.game = Game()

    def mainloop(self):

        screen = self.screen
        game = self.game
        displayBoard = self.game.displayBoard
        dragger = self.game.dragger

        while True:
            game.show_bg(screen)
            game.show_pieces(screen)

            if dragger.dragging:
                dragger.update_blit(screen)

            for event in pygame.event.get():

                # click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)

                    clicked_row = dragger.mouseY // SQSIZE
                    clicked_col = dragger.mouseX // SQSIZE

                    # if clicked square has piece
                    if displayBoard.squares[clicked_row][clicked_col].has_piece():
                        piece = displayBoard.squares[clicked_row][clicked_col].piece
                        dragger.save_initial(event.pos)
                        dragger.drag_piece(piece)

                # mouse motion
                elif event.type == pygame.MOUSEMOTION:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        #game.show_bg(screen)
                        #game.show_pieces(screen)
                        dragger.update_blit(screen)

                # click release
                elif event.type == pygame.MOUSEBUTTONUP:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                        released_row = dragger.mouseY // SQSIZE
                        released_col = dragger.mouseX // SQSIZE

                        startSquareName = displayBoard.CoordsToSquareName((dragger.initial_row,dragger.initial_col))
                        endSquareName = displayBoard.CoordsToSquareName((released_row,released_col))

                        if startSquareName != endSquareName:

                            proposedMove = startSquareName + endSquareName
                            #print('Proposed move: ' + proposedMove)

                            if chess.Move.from_uci(proposedMove) in displayBoard.activeBoard.legal_moves:
                                print("Making move " + proposedMove)

                                displayBoard.activeBoard.push_uci(proposedMove)
                                displayBoard._update_pieces()

                            else:
                                print("Move " + proposedMove + " is not legal")
                        

                    dragger.undrag_piece()

                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            pygame.display.update()



main = Main()
main.mainloop()