from socket import gaierror
import pygame
import sys
import chess


from const import *
from evaluation import *
from game import Game

class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode( (WIDTH + SIDEBARSIZE, HEIGHT) )
        pygame.display.set_caption('Chess')
        self.game = Game()

    def mainloop(self):

        screen = self.screen
        game = self.game
        displayBoard = self.game.displayBoard

        displayBoard.update_sidebar(screen)

        suggestedMove = 'e2e4'
        displayBoard.update_eval_indicator(screen, suggestedMove)

        dragger = self.game.dragger

        while True:
            game.show_bg(screen)
            game.show_pieces(screen)
            displayBoard.update_eval_indicator(screen, suggestedMove)

            if dragger.dragging:
                dragger.update_blit(screen)

            for event in pygame.event.get():

                # click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    # if clicked on the board
                    if event.pos[0] < COLS * SQSIZE:        
                        dragger.update_mouse(event.pos)

                        clicked_row = dragger.mouseY // SQSIZE
                        clicked_col = dragger.mouseX // SQSIZE

                        

                        # if clicked square has piece
                        if displayBoard.squares[clicked_row][clicked_col].has_piece():
                            piece = displayBoard.squares[clicked_row][clicked_col].piece
                            
                            if(displayBoard.flipped):
                                clicked_row = 7 - clicked_row
                                clicked_col = 7 - clicked_col

                            dragger.save_initial(clicked_row, clicked_col)
                            dragger.drag_piece(piece)

                    # if clicked 'Flip' button
                    elif self._is_pos_inside_rect(event.pos, displayBoard.flipButtonRect):
                        displayBoard.flip_board()
                        displayBoard._update_pieces()
                    
                   
                # mouse motion
                elif event.type == pygame.MOUSEMOTION:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        #game.show_bg(screen)
                        #game.show_pieces(screen)
                        dragger.update_blit(screen)


                # click release
                elif event.type == pygame.MOUSEBUTTONUP:
                    if dragger.dragging and event.pos[0] < COLS * SQSIZE:        # if dragging and released on the board:
                        dragger.update_mouse(event.pos)

                        released_row = dragger.mouseY // SQSIZE
                        released_col = dragger.mouseX // SQSIZE

                        if(displayBoard.flipped):
                            released_row = 7 - released_row
                            released_col = 7 - released_col

                        startSquareName = displayBoard.CoordsToSquareName((dragger.initial_row,dragger.initial_col))
                        endSquareName = displayBoard.CoordsToSquareName((released_row,released_col))

                        if startSquareName != endSquareName:

                            proposedMove = startSquareName + endSquareName
                            #print('Proposed move: ' + proposedMove)

                            legalMoveMade = False

                            if chess.Move.from_uci(proposedMove) in displayBoard.activeBoard.legal_moves:

                                # MAKE MOVE
                                print("Making move " + proposedMove)
                                displayBoard.activeBoard.push_uci(proposedMove)
                                legalMoveMade = True     

                            # queening pawn
                            elif chess.Move.from_uci(proposedMove + 'q') in displayBoard.activeBoard.legal_moves:
                                
                                # MAKE MOVE (queening)
                                print("Making move " + proposedMove + 'q')
                                displayBoard.activeBoard.push_uci(proposedMove + 'q')     
                                legalMoveMade = True 

                            else:
                                print("Move " + proposedMove + " is not legal")   


                            # if legal move has been made
                            if legalMoveMade:
                                displayBoard._update_pieces()

                                if(displayBoard.activeBoard.is_checkmate()):
                                    print('### Checkmate! ###')
                                else:

                                    ### EVALUATION ###

                                    eval = Evaluation()
                                    suggestedMove = eval.suggest_move(displayBoard.activeBoard)
                                    print('Suggesting move ' + suggestedMove)

                                    pass
                                    
                        

                    dragger.undrag_piece()

                    displayBoard.update_sidebar(screen)

                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            pygame.display.update()

    def _is_pos_inside_rect(self, pos, rect):
        if(
            pos[0] > rect[0] and pos[0] < rect[0] + rect[2] and
            pos[1] > rect[1] and pos[1] < rect[1] + rect[3]
        ): return True
        return False

main = Main()
main.mainloop()