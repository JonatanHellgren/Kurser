import numpy as np
"""
This is the state class, it was planned to be used in both the game and MCTS, it
however became a bit to complicated and with the deadline creeping up this did
not happen.  It has some useful properties tough. It is almost like the super
human part of the AI is that it is able to abrstact the game state as a state
object and thus look ahead more easier.
"""


class states():
    def __init__(self, mat):
        self.size = len(mat)
        self.state = mat

    """
    generates the legal moves from the current state
    """

    def get_legal_moves(self, value):
        legal = []
        for ix in range(self.size):
            for jx in range(self.size):
                if self.state[ix, jx] == 0:
                    tmp_state = np.copy(self.state)
                    tmp_state[ix, jx] = value
                    legal.append(tmp_state)
        return legal

    """
    A very simple way to see wheter or not a state is a terminal node, it only
    works when the board size is 3, however it is still possible ofcourse to use
    on larger boards, it is just that the games rules become a bit wierd.
    """

    def is_terminal(self):
        r = check_row(self.state)
        c = check_col(self.state)
        d = check_dig(self.state)
        full = check_full(self.state)
        if r[0]:
            return [True, r[1]]
        elif c[0]:
            return [True, c[1]]
        elif d[0]:
            return [True, d[1]]
        elif full:
            return [True, 0]
        else:
            return [False, 0]


""" 
same function as used in game.py
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
