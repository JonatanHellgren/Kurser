import random
import numpy as np
from MCTS import MCTS
"""
The game is implemented as a class, since that is what we liek to do after we
saw how important it was in the AI-tools lecture
"""


class TicTacToe():
    """
    Simple init function, with basically no options, you will be named player1
    and play agains the MCTS algorithm AInar
    """
    def __init__(self, size=3):
        self.board = np.zeros([size, size])
        self.sz = size
        self.players = [
            players('Player1', 'circle'),
            players('AInar', 'cross', is_AI=True)
        ]

    def start(self):
        self.print()
        current_player = self.players[0]
        for player in self.players:
            if player.is_AI:
                player.init_AI(self.board.copy())

        while not self.is_terminal()[0]:
            print(f"{current_player.name}'s turn")
            self.get_cord(current_player)
            self.print()
            current_player = self.next_player(current_player)
        print('game ended')

    def next_player(self, current_player):
        if current_player == self.players[0]:
            return self.players[1]
        else:
            return self.players[0]

    def get_cord(self, player):
        made_move = False
        while (not made_move):
            if player.is_AI:
                x, y = player.get_move(self.board)
                made_move = self.make_move(x, y, player)
            else:
                print(f'write where to place an {player.piece.symbol}')
                x = input("x-coordinate: ")
                x = int(x)
                y = input("Y-coordinate: ")
                y = int(y)
                made_move = self.make_move(x, y, player)

    def make_move(self, x, y, player):
        if self.in_bounds(x) and self.in_bounds(y) and self.board[x, y] == 0:
            self.board_set(x, y, player)
            return True
        else:
            return False

    def board_set(self, x, y, player):
        self.board[x, y] = player.piece.value

    def in_bounds(self, cord):
        return -1 < cord and cord < self.sz

    def is_terminal(self):
        r = check_row(self.board)
        c = check_col(self.board)
        d = check_dig(self.board)
        full = check_full(self.board)
        if r[0]:
            print('row')
            return [True, r[1]]
        elif c[0]:
            print('col')
            return [True, c[1]]
        elif d[0]:
            print('dig')
            return [True, d[1]]
        elif full:
            print('full')
            return [True, 0]
        else:
            return [False, 0]

    def print(self):
        for it, row in enumerate(self.board):
            draw_row(row)
            if it != self.sz - 1:  # if not last row
                draw_boundry(self.sz)


"""
This is the players class, not that much can be done here except giving them a
name a piece and a brain.
"""


class players():
    def __init__(self, name, symbol, is_AI=False):
        self.name = name
        self.piece = pieces(symbol, name)
        self.is_AI = is_AI

    def init_AI(self, state):
        self.brain = MCTS(state)

    def get_move(self, state):
        if self.is_AI:
            return self.brain.get_move(state)
        else:
            print('Dear player is not an AI, make your own move...')


class pieces():
    def __init__(self, symbol, owner):
        self.symbol = symbol
        self.owner = owner
        if self.symbol == 'circle':
            self.value = 1
        elif self.symbol == 'cross':
            self.value = -1
        else:
            print(f'Undefined symbol: {self.symbol}')


"""
Functions to draw the board in the terminal, very advanced graphics is used
here, so an dedicated graphics card is advised
"""


def draw_row(row):
    written = ""
    for it, cell in enumerate(row):
        if cell == 1:
            written += 'O'
        elif cell == -1:
            written += 'X'
        else:
            written += ' '
        if it != len(row) - 1:
            written += '|'
    print(written)


def draw_boundry(sz):
    written = ""
    for it in range(sz - 1):
        written += "-+"
    written += "-"
    print(written)


"""
Functions to determine is the boardstate is terminal or not
"""


def check_col(state):
    size = len(state)
    for it in range(size - 2):  #row
        for jt in range(size):  #col
            if state[it, jt] != 0:
                if (state[it, jt] == state[it + 1, jt]
                        and state[it + 2, jt] == state[it + 1, jt]):
                    return [True, state[it, jt]]
    return [False, 0]


def check_row(state):
    size = len(state)
    for it in range(size):  #row
        for jt in range(size - 2):  #col
            if state[it, jt] != 0:
                if (state[it, jt] == state[it, jt + 1]
                        and state[it, jt + 2] == state[it, jt + 1]):
                    return [True, state[it, jt]]
    return [False, 0]


def check_dig(state):
    size = len(state)
    for it in range(size - 2):
        for jt in range(size - 2):
            if state[it, jt] != 0:
                if (state[it, jt] == state[it + 1, jt + 1]
                        and state[it + 1, jt + 1] == state[it + 2, jt + 2]):
                    return [True, state[it, jt]]
            if state[size - it - 1, jt] != 0:
                if (state[size - it - 1, jt] == state[size - it - 2, jt + 1]
                        and state[size - it - 2,
                                  jt + 1] == state[size - it - 3, jt + 2]):
                    return [True, state[size - it - 1, jt]]
    return [False, 0]


def check_full(state):
    return 0 not in state
