import pygame
import chess
import random

from const import *

class Evaluation:

    def __init__(self):
        pass

    def suggest_move(self, board):
        #return self.RANDOM_MOVE(board)
        return self.CAPTURE_PIECES(board)






    def CAPTURE_PIECES(self, board):
        legalMovesList = list(board.legal_moves)

        initialMatBalance = self.material_balance(board)
        moveMatBalanceList = []
        
        for move in legalMovesList:
            board.push(move)
            moveMatBalanceList.append(self.material_balance(board))
            board.pop()
        
        if board.turn == chess.WHITE:
            index_max = max(range(len(moveMatBalanceList)), key=moveMatBalanceList.__getitem__)
            if moveMatBalanceList[index_max] > initialMatBalance:
                return str(legalMovesList[index_max])            
        else:
            index_min = min(range(len(moveMatBalanceList)), key=moveMatBalanceList.__getitem__)
            if moveMatBalanceList[index_min] < initialMatBalance:
                return str(legalMovesList[index_min])

        # if no move helps mat balance, make random move
        return self.RANDOM_MOVE(board)



    def RANDOM_MOVE(self, board):
        legalMovesList = list(board.legal_moves)

        r = random.randint(0,len(legalMovesList) - 1)

        #print('current mat balance: ' + str(self.material_balance(board)))

        return str(legalMovesList[r])


    def material_balance(self, board):
        white = board.occupied_co[chess.WHITE]
        black = board.occupied_co[chess.BLACK]
        return (
            chess.popcount(white & board.pawns) - chess.popcount(black & board.pawns) +
                3 * (chess.popcount(white & board.knights) - chess.popcount(black & board.knights)) +
                3 * (chess.popcount(white & board.bishops) - chess.popcount(black & board.bishops)) +
                5 * (chess.popcount(white & board.rooks) - chess.popcount(black & board.rooks)) +
                9 * (chess.popcount(white & board.queens) - chess.popcount(black & board.queens))
            )