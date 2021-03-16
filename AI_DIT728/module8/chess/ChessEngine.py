"""
This class is responsible for storing the information about the state of the
current chess game
Also resposible for determening the valid moves at the current state, will also
keep a move Log.
"""
import numpy as np


class GameState():
    def __init__(self):
        #board 8x8 2d numpy array of string with two characters
        # first character represents color
        # second character represents type
        # rook(R), knight(N), bishop(B), queen(Q), king(K), pawn(p)
        self.board = np.array(
            [["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
             ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
             ["--", "--", "--", "--", "--", "--", "--", "--"],
             ["--", "--", "--", "--", "--", "--", "--", "--"],
             ["--", "--", "--", "--", "--", "--", "--", "--"],
             ["--", "--", "--", "--", "--", "--", "--", "--"],
             ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
             ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]])
        '''
        self.board = np.array(
            [["--", "--", "--", "--", "--", "--", "--", "--"],
             ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
             ["--", "--", "--", "--", "--", "--", "--", "--"],
             ["--", "--", "--", "bK", "--", "wK", "--", "--"],
             ["--", "--", "--", "--", "--", "--", "--", "--"],
             ["--", "--", "--", "--", "--", "--", "--", "--"],
             ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
             ["--", "--", "--", "--", "--", "--", "--", "--"]])
        '''
        self.moveFunctions = {
            'p': self.getPawnMoves,
            'R': self.getRookMoves,
            'B': self.getBishopMoves,
            'Q': self.getQueenMoves,
            'N': self.getKnightMoves,
            'K': self.getKingMoves
        }
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.inCheck = False
        self.pins = []
        self.checks = []
        self.checkMate = False
        self.staleMate = False

        # en passnt
        self.enPassantPossible = ()  # coordinates of possible en passants

        # castling
        self.currentCastleRight = CastleRights(True, True, True, True)
        self.castleRightsLog = []
        self.castleRightsLog.append(
            CastleRights(self.currentCastleRight.wks,
                         self.currentCastleRight.bks,
                         self.currentCastleRight.wqs,
                         self.currentCastleRight.bqs))

    '''
    Move function, takes a move object and executes the move on the board
    '''

    def makeMove(self, move):
        self.board[move.startRow, move.startCol] = "--"
        self.board[move.endRow, move.endCol] = move.pieceMoved
        self.moveLog.append(move)  # log the move so we can undo it
        self.whiteToMove = not self.whiteToMove  # next turn

        # if king was moved
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)

        # when pawn does two quare move add possible enPassant
        if move.pieceMoved[1] == 'p' and \
                abs(move.startRow - move.endRow) == 2:
            self.enPassantPossible = ((move.endRow + move.startRow) // 2,
                                      move.endCol)
        else:
            self.enPassantPossible = ()

        # if move was an enPassant remove the targeted piece
        if move.enPassant:
            self.board[move.startRow, move.endCol] = "--"

        # when pawn has reached backrow promote it
        if move.pawnPromotion:
            # only makes the pawn a queen for simplicity
            self.board[move.endRow, move.endCol] = move.pieceMoved[0] + 'Q'

        if move.isCastleMove:
            if move.endCol - move.startCol == 2:
                self.board[move.endRow,
                           move.endCol - 1] = self.board[move.endRow,
                                                         move.endCol + 1]
                self.board[move.endRow, move.endCol + 1] = "--"
            else:
                self.board[move.endRow, move.endCol + 1] = \
                    self.board[move.endRow, move.endCol - 2]
                self.board[move.endRow, move.endCol - 2] = "--"

        # castling rights - when king or rook moves
        self.updateCastleRights(move)

    '''
    Undo last move
    '''

    def undoMove(self):
        if len(self.moveLog) != 0:  # if there is a move to undo
            move = self.moveLog.pop()
            self.board[move.startRow, move.startCol] = move.pieceMoved
            self.board[move.endRow, move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove  # switch turn back
            # update kings position
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)
            if move.enPassant:
                # leave landing square blank
                self.board[move.endRow, move.endCol] = "--"
                self.board[move.startRow, move.endCol] = move.pieceCaptured
                self.enPassantPossible = (move.endRow, move.endCol)
            # undo a 2 square pawn advance
            if move.pieceMoved[1] == 'p' and \
                    abs(move.startRow - move.endRow) == 2:
                self.enpasantPossible = ()
            # undo castle move
            # undo castlering rights
            self.castleRightsLog.pop()  # remove old
            new = self.castleRightsLog[-1]
            self.currentCastleRight = CastleRights(new.wks, new.bks, new.wqs,
                                                   new.bqs)
            if move.isCastleMove:
                if move.endCol - move.startCol == 2:  #kingside
                    self.board[move.endRow, move.endCol + 1] = \
                        self.board[move.endRow, move.endCol-1]
                    self.board[move.endRow, move.endCol - 1] = "--"
                else:  # queen side
                    self.board[move.endRow, move.endCol -2] = \
                        self.board[move.endRow, move.endCol + 1]
                    self.board[move.endRow, move.endCol + 1] = "--"

    '''
    Update the castle rights
    '''

    def updateCastleRights(self, move):
        # if a rook was moved
        if move.pieceMoved == 'wK':
            self.currentCastleRight.wks = False
            self.currentCastleRight.wqs = False
        elif move.pieceMoved == 'bK':
            self.currentCastleRight.bks = False
            self.currentCastleRight.bqs = False
        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startCol == 0:  # left rook
                    self.currentCastleRight.wqs = False
                elif move.startCol == 7:  # right rook
                    self.currentCastleRight.wks = False
        elif move.pieceMoved == 'bR':
            if move.startRow == 0:
                if move.startCol == 0:  # left rook
                    self.currentCastleRight.bqs = False
                elif move.startCol == 7:  # right rook
                    self.currentCastleRight.bks = False

        # if a rook was captured
        if move.pieceCaptured == 'wR':
            if move.endRow == 7:
                if move.endCol == 0:
                    self.currentCastleRight.wqs = False
                elif move.endCol == 7:
                    self.currentCastleRight.wks = False
        elif move.pieceCaptured == 'bR':
            if move.endRow == 0:
                if move.endCol == 0:
                    self.currentCastleRight.bqs = False
                elif move.endCol == 7:
                    self.currentCastleRight.bks = False

        # update the log
        self.castleRightsLog.append(
            CastleRights(self.currentCastleRight.wks,
                         self.currentCastleRight.bks,
                         self.currentCastleRight.wqs,
                         self.currentCastleRight.bqs))

    '''
    All moves that won't result in a check
    Removing the ability for moving pinned pieces and moving King into check
    '''

    def getValidMoves(self):
        moves = []
        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()
        if self.whiteToMove:
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]
        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]
        if self.inCheck:
            # only one check, block check or move king
            if len(self.checks) == 1:
                moves = self.getAllPossibleMoves()
                # to block a check you must move a piece into one of the squares
                # between the enemy piece and the king
                check = self.checks[0]
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow,
                                           checkCol]  # checking piece
                validSquares = []  # squares that pieces can move to
                # if knight, must capture knight or move king
                if pieceChecking[1] == 'N':
                    validSquares = [(checkRow, checkCol)]
                else:
                    for i in range(1, 8):
                        validSquare = (kingRow + check[2] * i,
                                       kingCol + check[3] * i)
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and \
                                validSquare[1] == checkCol:
                            # once you get to piece end checks
                            break
                # get rid of any moves that don't block check or move king
                for i in range(len(moves) - 1, -1, -1):
                    if moves[i].pieceMoved[1] != 'K':
                        if not (moves[i].endRow, moves[i].endCol) in \
                                validSquares:
                            moves.remove(moves[i])
            else:  # double check, king has to move
                self.getKingMoves(kingRow, kingCol, moves)
        else:  # not in check so all moves are fine
            moves = self.getAllPossibleMoves()

        if len(moves) == 0:
            if self.inCheck:
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False

        # only kings left on board: stalemate
        if np.sum(self.board != '--') <= 2:
            self.staleMate = True

        return moves

    '''
    All moves without considering checks
    '''

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):  # rows
            for c in range(len(self.board[r])):  # columns
                turn = self.board[r,
                                  c][0]  # color of the player wich turn it is
                if (turn == 'w'
                        and self.whiteToMove) or (turn == 'b'
                                                  and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)
        return moves

    '''
    Returns if the player i in check, a list of pins, and a list of checks
    '''

    def checkForPinsAndChecks(self):
        pins = []
        checks = []
        inCheck = False
        if self.whiteToMove:
            enemyColor = "b"
            allyColor = "w"
            startRow = self.whiteKingLocation[0]
            startCol = self.whiteKingLocation[1]
        else:
            enemyColor = "w"
            allyColor = "b"
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1),
                      (1, -1), (1, 1))
        for j in range(len(directions)):
            d = directions[j]
            possiblePin = ()  # reset possible pin
            for i in range(1, 8):
                endRow = startRow + d[0] * i
                endCol = startCol + d[1] * i
                if inBounds(endRow, endCol, self.board):
                    endPiece = self.board[endRow, endCol]
                    if endPiece[0] == allyColor and endPiece[1] != 'K':
                        if possiblePin == (
                        ):  # 1st allied piece could be pinned
                            possiblePin = (endRow, endCol, d[0], d[1])
                        else:
                            # 2nd piece in row, so first can't be a pin
                            break
                    elif endPiece[0] == enemyColor:
                        type = endPiece[1]
                        # 5 possibilities here
                        # 1. orthogonally away from king and piece is a rook
                        # 2. diagonally away from king and piece is a bishop
                        # 3. 1 square away from king  and piece is a pawn
                        # 4. any direction and piece is queen
                        # 5. an direction 1 square away and piece is a king
                        if (0 <= j <= 3 and type == 'R') or \
                                (4 <= j <= 7 and type == 'B') or \
                                (i == 1 and type == 'p' and \
                                 ((enemyColor == 'w' and 6 <= j <= 7) or \
                                  (enemyColor == 'b' and 4 <= j <= 5))) or \
                                (type == 'Q') or (i == 1 and type == 'K'):
                            if possiblePin == ():  # no piece blocking
                                inCheck = True
                                checks.append((endRow, endCol, d[0], d[1]))
                                break
                            else:  # piece is blocking so pin
                                pins.append(possiblePin)
                                break
                        else:  # enemy piece not applying check
                            break
                else:
                    break  # off board
        # check for knight checks
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2),
                       (2, -1), (2, 1))
        for m in knightMoves:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if inBounds(endRow, endCol, self.board):
                endPiece = self.board[endRow, endCol]
                if endPiece[0] == enemyColor and endPiece[1] == 'N':
                    inCheck = True
                    checks.append((endRow, endCol, m[0], m[1]))
        return inCheck, pins, checks

    '''
    Get piece moves located at row, col and add these moves to the list
    '''

    def getPawnMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        if self.whiteToMove:
            moveAmount = -1
            startRow = 6
            backRow = 0
            enemyColor = 'b'
        else:
            moveAmount = 1
            startRow = 1
            backRow = 7
            enemyColor = 'w'
        pawnPromotion = False

        if self.board[r + moveAmount, c] == "--":  # 1 square
            if not piecePinned or pinDirection == (moveAmount, 0):
                if r + moveAmount == backRow:  # promote if reached backRow
                    pawnPromotion = True
                moves.append(
                    Move((r, c), (r + moveAmount, c),
                         self.board,
                         pawnPromotion=pawnPromotion))
                if r == startRow and self.board[r + 2 * moveAmount, c] == "--":
                    moves.append(
                        Move((r, c), (r + 2 * moveAmount, c), self.board))
        if c > -1:  # capture to the left
            if not piecePinned or pinDirection == (moveAmount, -1):
                if self.board[r + moveAmount, c - 1][0] == enemyColor:
                    if r + moveAmount == backRow:
                        pawnPromotion = True
                    moves.append(
                        Move((r, c), (r + moveAmount, c - 1),
                             self.board,
                             pawnPromotion=pawnPromotion))
                if (r + moveAmount, c - 1) == self.enPassantPossible:
                    moves.append(
                        Move((r, c), (r + moveAmount, c - 1),
                             self.board,
                             enPassant=True))
        if c < 7:  # capture to the right
            if not piecePinned or pinDirection == (moveAmount, -1):
                if self.board[r + moveAmount, c + 1][0] == enemyColor:
                    if r + moveAmount == backRow:
                        pawnPromotion = True
                    moves.append(
                        Move((r, c), (r + moveAmount, c + 1),
                             self.board,
                             pawnPromotion=pawnPromotion))
                if (r + moveAmount, c + 1) == self.enPassantPossible:
                    moves.append(
                        Move((r, c), (r + moveAmount, c + 1),
                             self.board,
                             enPassant=True))

    def getBishopMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        color = self.board[r, c][0]
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if inBounds(endRow, endCol, self.board):
                    if not piecePinned or pinDirection == d \
                            or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow, endCol]
                        if endPiece == "--":  # empty swuare
                            moves.append(
                                Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] != color:  # enemy piece
                            moves.append(
                                Move((r, c), (endRow, endCol), self.board))
                            break
                        else:  # friendly piece
                            break
                else:  # off board
                    break

    def getRookMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if self.board[r, c][1] != 'Q':
                    self.pins.remove(self.pins[i])
                break

        color = self.board[r, c][0]
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if inBounds(endRow, endCol, self.board):
                    if not piecePinned or pinDirection == d \
                            or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow, endCol]
                        if endPiece == "--":  # empty swuare
                            moves.append(
                                Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] != color:  # enemy piece
                            moves.append(
                                Move((r, c), (endRow, endCol), self.board))
                            break
                        else:
                            break
                else:  # off board
                    break

    def getKnightMoves(self, r, c, moves):
        piecePinned = False
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                self.pins.remove(self.pins[i])
                break

        color = self.board[r, c][0]
        offsets = [[2, -1], [2, 1], [-2, 1], [-2, -1], [1, -2], [1, 2],
                   [-1, 2], [-1, -2]]
        for offset in offsets:
            if inBounds(r + offset[0], c + offset[1], self.board):
                if not piecePinned:
                    if self.board[r + offset[0], c + offset[1]][0] != color:
                        moves.append(
                            Move((r, c), (r + offset[0], c + offset[1]),
                                 self.board))

    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)
        return moves

    def getKingMoves(self, r, c, moves):
        rowMoves = (-1, -1, -1, 0, 0, 1, 1, 1)
        colMoves = (-1, 0, 1, -1, 1, -1, 0, 1)
        allyColor = self.board[r, c][0]
        for i in range(8):
            endRow = r + rowMoves[i]
            endCol = c + colMoves[i]
            if inBounds(endRow, endCol, self.board):
                endPiece = self.board[endRow, endCol]
                if endPiece[0] != allyColor:
                    # place king on square and check for checks
                    if allyColor == 'w':
                        self.whiteKingLocation = (endRow, endCol)
                    else:
                        self.blackKingLocation = (endRow, endCol)
                    inCheck, pins, checks = self.checkForPinsAndChecks()
                    if not inCheck:
                        moves.append(Move((r, c), (endRow, endCol),
                                          self.board))
                    # place king on back on original location
                    if allyColor == 'w':
                        self.whiteKingLocation = (r, c)
                    else:
                        self.blackKingLocation = (r, c)

        inCheck, pins, checks = self.checkForPinsAndChecks()
        if not inCheck:  # can't castle if in check
            self.getCastleMoves(r, c, moves, allyColor)

    """
    Generate all valid castle moves for the king
    """

    def getCastleMoves(self, r, c, moves, allyColor):
        # check king side castling
        if (self.whiteToMove and self.currentCastleRight.wks) or \
                (not self.whiteToMove and self.currentCastleRight.bks):
            self.getKingSideCastleMoves(r, c, moves, allyColor)
        # check queen side castling
        if (self.whiteToMove and self.currentCastleRight.wqs) or \
                (not self.whiteToMove and self.currentCastleRight.bqs):
            self.getQueenSideCastleMoves(r, c, moves, allyColor)

    def getKingSideCastleMoves(self, r, c, moves, allyColor):
        if self.board[r, c + 1] == "--" and self.board[r, c + 2] == "--" and \
                not self.isUnderAttack(r, c +1, allyColor) \
                and not self.isUnderAttack(r, c +2, allyColor):
            if allyColor == 'w' and self.currentCastleRight.wks or \
                    allyColor == 'b' and self.currentCastleRight.bks:
                moves.append(
                    Move((r, c), (r, c + 2), self.board, isCastleMove=True))

    def getQueenSideCastleMoves(self, r, c, moves, allyColor):
        if self.board[r, c -1] == "--" and self.board[r, c -2] == "--" and \
                self.board[r, c -3] == "--" and \
                not self.isUnderAttack(r, c -1, allyColor) \
                and  not self.isUnderAttack(r, c -2, allyColor):
            if allyColor == 'w' and self.currentCastleRight.wqs or \
                    allyColor == 'b' and self.currentCastleRight.bqs:
                moves.append(
                    Move((r, c), (r, c - 2), self.board, isCastleMove=True))

    def isUnderAttack(self, r, c, allyColor):
        underAttack = False
        directions = ((1, 0), (-1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            d = directions[j]
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if inBounds(endRow, endCol, self.board):
                    endPiece = self.board[endRow, endCol]
                    if endPiece[0] == allyColor:
                        break
                    elif endPiece[0] != '-':
                        type = endPiece[1]
                        if (0 <= j <= 1 and type == 'R') or \
                                (2 <= j <= 5 and type == 'B') or \
                                (i == 1 and type == 'p' and \
                                 ((allyColor == 'w' and 4 <= j <= 5) or \
                                  (allyColor == 'b' and 2 <= j <= 3))) or \
                                (type == 'Q') or (i == 1 and type == 'K'):
                            underAttack = True
                            break
        # check for knight checks
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2),
                       (2, -1), (2, 1))
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if inBounds(endRow, endCol, self.board):
                endPiece = self.board[endRow, endCol]
                if endPiece[0] != allyColor and endPiece[1] == 'N':
                    underAttack = True
        return underAttack


def inBounds(r, c, board):
    max_r, max_c = board.shape
    if -1 < r and r < max_r and -1 < c and c < max_c:
        return True
    return False


class CastleRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs


"""
Move class, this is how we will store the moves.
We store the start and end possition for the move, also wheter the move is a
pwan promotion, en passant or a casteling move
"""


class Move():
    ranksToRows = {
        '1': 7,
        '2': 6,
        '3': 5,
        '4': 4,
        '5': 3,
        '6': 2,
        '7': 1,
        '8': 0
    }
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {
        'a': 0,
        'b': 1,
        'c': 2,
        'd': 3,
        'e': 4,
        'f': 5,
        'g': 6,
        'h': 7
    }
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self,
                 startSq,
                 endSq,
                 board,
                 pawnPromotion=False,
                 enPassant=False,
                 isCastleMove=False):

        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow, self.startCol]
        self.pieceCaptured = board[self.endRow, self.endCol]
        # pawn promotion
        self.pawnPromotion = pawnPromotion
        # en passant
        self.enPassant = enPassant
        if enPassant:
            self.pieceCaptured = 'bp' if self.pieceMoved == 'wp' else 'wp'
        self.moveID = self.startRow * 1000 + self.startCol * 100 + \
            self.endRow * 10 + self.endCol
        self.isCastleMove = isCastleMove

    '''
    Overriding the equals method 
    '''

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        piece = self.pieceMoved[1]
        if piece != 'p':
            return piece + self.getRankFile(self.endRow, self.endCol)
        else:
            return self.getRankFile(self.endRow, self.endCol)


    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]


# stop word
