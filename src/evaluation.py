import pygame
import chess
import random

from const import *

class Evaluation:

    def __init__(self):
        pass

    def suggest_move(self, board):
        legalMovesList = list(board.legal_moves)

        r = random.randint(0,len(legalMovesList) - 1)

        return str(legalMovesList[r])