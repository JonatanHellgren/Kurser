import random
import pandas as pd


def findRandomMove(validMoves):
    i = random.randint(0, len(validMoves) - 1)
    return validMoves[i]


