import numpy as np
from tic_tac_toe import TicTacToe


def main():
    game = TicTacToe(size=3, mode='MCTS')

    game.start()


if __name__ == "__main__":
    main()
