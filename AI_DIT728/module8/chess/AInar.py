import random


def findRandomMove(validMoves):
    i = random.randint(0, len(validMoves) - 1)
    return validMoves[i]


def findBestMove():
    pass
