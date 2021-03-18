import pandas as pd
import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense


def main():
    '''
    x, y1, y2 = get_data()
    model = simple_model()
    model.fit(x, y2, epochs=10, batch_size=100)
    '''
    pass


def simple_model():
    model = Sequential()
    model.add(Dense(800, input_dim=773, activation='relu'))
    model.add(Dense(400, activation='relu'))
    model.add(Dense(400, activation='relu'))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    return model


def get_data():
    df = pd.read_csv('~/Data/chessData_e5.csv')
    X_data = []
    Y_check = []
    Y_score = []
    for it in range(df.shape[0]):
        print(it)
        X_data.append(FEN_to_bitmap(df.iloc[it, 0]))
        forced_mate, score = get_evaluation(df.iloc[it, 1])
        Y_check.append(forced_mate)
        Y_score.append(score)
    return np.array(X_data), np.array(Y_check), np.array(Y_score)


def get_evaluation(Evaluation):
    forced_mate = 0
    if '#' in Evaluation:
        forced_mate = 1
        Evaluation = Evaluation[1:]
    return forced_mate, int(Evaluation)


def FEN_to_board():
    df = pd.read_csv('chessData_100.csv')
    return bitmap_to_board(FEN_to_bitmap(df.iloc[60, 0]))


'''
A funtction that takes an FEN input and rturns a bit map projection of size 773
'''


def FEN_to_bitmap(FEN_string):
    state, turn, castle = FEN_string.split()[0:3]
    pieces = np.array(
        ['P', 'N', 'B', 'R', 'Q', 'K', 'p', 'n', 'b', 'r', 'q', 'k'])
    # add player turn
    if turn == 'w':
        bitmap = np.array([1])
    else:
        bitmap = np.array([0])
    state = state.split('/')

    # add castle rights
    bitmap = np.concatenate((bitmap, np.zeros((4))))
    castles = ['K', 'k', 'Q', 'q']
    for it, castle_right in enumerate(castles):
        if castle_right in castle:
            bitmap[it + 1] = 1

    # add piece positions
    for row in state:
        for c in row:
            if c in pieces:
                bit = np.zeros((12))
                ind = np.where(c == pieces)[0][0]
                bit[ind] = 1
                bitmap = np.concatenate((bitmap, bit))
            else:
                empty = int(c)
                bits = np.zeros((12 * empty))
                bitmap = np.concatenate((bitmap, bits))
    return bitmap.astype('int8')


def bitmap_to_board(bitmap):
    pieces = np.array([
        'wp', 'wN', 'wB', 'wR', 'wQ', 'wK', 'bp', 'bN', 'bB', 'bR', 'bQ', 'bK'
    ])
    board = np.array([['--', '--', '--', '--', '--', '--', '--', '--'],
                      ['--', '--', '--', '--', '--', '--', '--', '--'],
                      ['--', '--', '--', '--', '--', '--', '--', '--'],
                      ['--', '--', '--', '--', '--', '--', '--', '--'],
                      ['--', '--', '--', '--', '--', '--', '--', '--'],
                      ['--', '--', '--', '--', '--', '--', '--', '--'],
                      ['--', '--', '--', '--', '--', '--', '--', '--'],
                      ['--', '--', '--', '--', '--', '--', '--', '--']])
    for row in range(8):
        for col in range(8):
            ind = 12 * (8 * row + col) + 5
            bit = bitmap[ind:ind + 12]
            if 1 in bit:
                board[row, col] = pieces[np.where(1 == bit)[0][0]]
    return board


if __name__ == '__main__':
    main()
    ad -y /tmp/nvimMWOAhr/234.ipy
    
