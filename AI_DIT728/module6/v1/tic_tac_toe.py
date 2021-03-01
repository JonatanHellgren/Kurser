import numpy as np
from MCTS import MCTS


class TicTacToe():
    def __init__(self, size=3, mode='1v1'):
        self.mode = mode
        self.sz = size
        self.board = np.zeros([self.sz, self.sz])

    def start(self):
        if self.mode == '1v1':
            self.simple()
        elif self.mode == 'MCTS':
            self.MCTS()

    def MCTS(self):
        turn = 0
        self.printBoard()
        AI = MCTS()
        while (not self.check_win()):
            self.draw('circle')
            self.printBoard()
            turn += 1
            AI_move = AI.get_move(self.board)
            print(AI_move)
            self.make_move(AI_move[0], AI_move[1], 'cross')
            self.printBoard()
            turn += 1

    def simple(self):
        symbols = ['circle', 'cross']
        symbol = symbols[0]
        turn = 0
        self.printBoard()
        while (not self.check_win()):
            self.draw(symbol)
            self.printBoard()
            turn += 1
            symbol = symbols[turn % 2]
            if check_if_end(turn):
                break

    def check_if_end(self, turn):
        if (turn == self.sz**2):
            print("!!!Failure!!! You ran out of moves!")
            return True
        else:
            return False

    def printBoard(self):
        for it, row in enumerate(self.board):
            draw_row(row)
            if it != self.sz - 1:  # if not last row
                draw_boundry(self.sz)

    def set_board(self, mat):
        self.board = mat

    def is_valid_cord(self, cord):
        return -1 < cord and cord < self.sz

    def draw(self, symbol):
        made_move = False
        while (not made_move):
            print(f'write where to place an {symbol}')
            x = input("x-coordinate: ")
            x = int(x)
            y = input("Y-coordinate: ")
            y = int(y)
            made_move = self.make_move(x, y, symbol)

    def make_move(self, x, y, symbol):
        if self.is_valid_cord(x) and self.is_valid_cord(y):
            if self.board[x, y] == 0:
                if symbol == 'circle':
                    self.board[x, y] = 1
                    return True
                elif symbol == 'cross':
                    self.board[x, y] = -1
                    return True
            else:
                print('Invalid coordianate')
                return False
        else:
            print('Invalid coordianate')
            return False

    def check_win(self):
        p1_txt = "Congratulations, you have succesed with outsmaring your computational overloard!!!"
        p2_txt = "!!!Failure!!! The AI outsmarted you!"
        for it in range(self.sz):
            row_sum = np.sum(self.board[it, :])
            col_sum = np.sum(self.board[:, it])
            if row_sum == 3 or col_sum == 3:
                print(p1_txt)
                return True
            elif row_sum == -3 or col_sum == -3:
                print(p2_txt)
                return True
        dig_sum1 = self.board[0, 0] + self.board[1, 1] + self.board[2, 2]
        dig_sum2 = self.board[0, 2] + self.board[1, 1] + self.board[2, 0]
        if dig_sum1 == 3 or dig_sum2 == 3:
            print(p1_txt)
            return True
        elif dig_sum1 == -3 or dig_sum2 == -3:
            print(p2_txt)
            return True
        return False


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
