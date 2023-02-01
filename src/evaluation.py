import pygame
import chess
import random
import datetime
import os

from const import *
from datetime import datetime

class Evaluation:

    def __init__(self):
        pass

    def suggest_move(self, board):
        #return self.RANDOM_MOVE(board)
        #return self.CAPTURE_PIECES(board)
        return self.MIN_MAX(board)





    def MIN_MAX(self, board):

        legalMovesList = list(board.legal_moves)  
        
        depth = 4       # depth = how many moves ahead to look (must be greater than 0)

        moveValueList = []

        inital_mat_balance = self.material_balance(board)

        os.system('cls')

        beforeTime = datetime.now()
        for move in legalMovesList:
            board.push(move)

            # if considered move is a capture, look one move deeper
            if(self.material_balance(board) != inital_mat_balance):
                moveValueList.append(self._position_value(board, depth))
            else:
                moveValueList.append(self._position_value(board, depth - 1))
            
            self.show_eval_progress(len(moveValueList), len(legalMovesList))
            
            board.pop()
        afterTime = datetime.now()

        os.system('cls')

        #just for debug / looking
        #for i in range(0,len(legalMovesList)):
            #print('move ' + str(legalMovesList[i]) + ' value: ' + str(moveValueList[i]))
        
        secondsThinking = (afterTime - beforeTime).total_seconds()
        print('Analyzed ' + str(len(legalMovesList)) + ' moves for ' + str(secondsThinking)[:4] + 's at depth '+ str(depth))
        print('(' + str(secondsThinking / float(len(legalMovesList)))[:4] + 's per move)')
        
        moveOptions = []
        index_ideal = -1

        # if white, consider only best options for white
        if board.turn == chess.WHITE:
            for i in range(0,len(legalMovesList)):
                if(moveValueList[i] == max(moveValueList)):
                    moveOptions.append(legalMovesList[i])
            
            # out of 'optimal' moves, choose the move with the most immediate material compensation
            moveMatBalanceList = []       
            for move in moveOptions:
                board.push(move)
                moveMatBalanceList.append(self.material_balance(board))
                board.pop()
            # if 'optimal' move exists that captures immediately, mark it. If not, leave index_ideal as -1 so random move can be chosen
            if max(moveMatBalanceList) > inital_mat_balance:
                index_ideal = max(range(len(moveMatBalanceList)), key=moveMatBalanceList.__getitem__)
            
        
        # if black, consider only best options for black 
        else:
            for i in range(0,len(legalMovesList)):
                if(moveValueList[i] == min(moveValueList)):
                    moveOptions.append(legalMovesList[i])
            
            # out of 'optimal' moves, choose the move with the most immediate material compensation
            moveMatBalanceList = []       
            for move in moveOptions:
                board.push(move)
                moveMatBalanceList.append(self.material_balance(board))
                board.pop()
            # if 'optimal' move exists that captures immediately, mark it. If not, leave index_ideal as -1 so random move can be chosen
            if min(moveMatBalanceList) < inital_mat_balance:
                index_ideal = min(range(len(moveMatBalanceList)), key=moveMatBalanceList.__getitem__)


        #just for debug / looking
        #print('move options:')
        #for option in moveOptions:
        #   print(str(option))       

        # if "optimal" immediate capture move was marked, play that move
        if(index_ideal > -1):
            return str(moveOptions[index_ideal])
        
        # return random move from set of moves that are optimal value
        r = random.randint(0,len(moveOptions) - 1)
        return str(moveOptions[r])

    
    # recursive method for minmax
    def _position_value(self, board, depth):

        if board.is_checkmate():
            if board.turn:  # if white has been mated
                return -99
            else:           # if black has been mated
                return 99
        
        if board.is_stalemate():
            return 0
        
        if depth < 1:
            return self.material_balance(board)

        # recursive step

        legalMovesList = list(board.legal_moves)
        
        boardValueList = []

        for move in legalMovesList:
            board.push(move)
            boardValueList.append(self._position_value(board, depth - 1))         
            board.pop()
        
        
        if board.turn == chess.WHITE:
            return max(boardValueList)         
        else:
            return min(boardValueList)    


    def show_eval_progress(self, current, total):
        os.system('cls')
        currentProgress = '|' * current
        remainingProgress = '.' * (total - current)
        percent = int((current / (total)) * 100)
        print('Evaluating position: ###' + currentProgress + remainingProgress + '###   ' + str(percent) + ' %')   
                






    def CAPTURE_PIECES(self, board):
        legalMovesList = list(board.legal_moves)

        initialMatBalance = self.material_balance(board)
        moveMatBalanceList = []
        
        for move in legalMovesList:
            board.push(move)

            # return move if immediately determined it is mate in 1
            if board.is_checkmate(): 
                board.pop()
                return str(move)

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