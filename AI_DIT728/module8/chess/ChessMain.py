"""
This is our main driver file. It will be responsible for handling user input and
displaying the current GameState object
"""
import pygame as p
from ChessEngine import GameState, Move
from AInar import findRandomMove
from NNtraining import FEN_to_board

WIDTH = HEIGHT = 800  #512
DIMENSION = 8  # 8x8 chess board
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 60  # animation speed
IMAGES = {}
"""
Initalize a global dictonary of images. This will be called exactly once in the
main
"""

def loadImages():
    pieces = [
        "wp", "wR", "wN", "wB", "wK", "wQ", "bp", "bR", "bN", "bB", "bK", "bQ"
    ]
    for piece in pieces:
        # loads imagaes and scales the to the square size
        img = p.image.load("images/" + piece + "2.png").convert()
        img.set_colorkey((239, 64, 34))  # for transparent background
        IMAGES[piece] = p.transform.scale(img, (SQ_SIZE, SQ_SIZE))


"""
The main driver for our code. THis will handle user u=input and updating the
grapics
"""


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = GameState()
    gs.board = FEN_to_board()
    validMoves = gs.getValidMoves()
    moveMade = False  # flag variable for when a move is made
    animate = False  # flag for when animations is being made
    gameOver = False

    loadImages()  # load images before the game starts
    running = True
    sqSelected = ()  # no square selected initially (tuple (row, col))
    playerClicks = []  # keeps track of player clicks, two tupels
    playerOne = True  # human is white, then this will be True
    playerTwo = True  # simiar as playerOne but for black
    while running:
        isHumanTurn = (gs.whiteToMove and playerOne) or \
            (not gs.whiteToMove and playerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and isHumanTurn:
                    location = p.mouse.get_pos()  #(x, y) loc of mouse click
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if sqSelected == (row, col):
                        sqSelected = ()  # delselect
                        playerClicks = []  # reset player clicks
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)  # append both clicks
                    if len(playerClicks) == 2:  # after 2nd click
                        move = Move(playerClicks[0], playerClicks[1], gs.board)
                        print(move.getChessNotation())
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveMade = True
                                animate = True
                                sqSelected = ()  # reset user clicks
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]
            # key handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # if press z, undo
                    gs.undoMove()
                    moveMade = True
                    animate = False
                if e.key == p.K_r:
                    gs = GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
        # AI move finder
        if not gameOver and not isHumanTurn:
            AIMove = findRandomMove(validMoves)
            gs.makeMove(AIMove)
            moveMade = True
            animate = True

        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs, validMoves, sqSelected)

        if gs.checkMate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, 'Black wins by checkmate')
            else:
                drawText(screen, 'White wind by checkmate')
        elif gs.staleMate:
            gameOver = True
            drawText(screen, 'stalemate')

        clock.tick(MAX_FPS)
        p.display.flip()


"""
Responsible for all the grapics within a current game state
"""


def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen)  # draw the squares on the board
    highlightLastMove(screen, gs)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)  # draw pieces on the board


"""
Draw squares on the board
"""


def drawBoard(screen):
    global colors
    colors = [p.Color("#ebdbb2"), p.Color("#928374")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            p.draw.rect(screen, color,
                        p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


'''
Highlighting the last move that the oppostie played made
'''


def highlightLastMove(screen, gs):
    if len(gs.moveLog) > 0:
        r, c = gs.moveLog[-1].endRow, gs.moveLog[-1].endCol
        s = p.Surface((SQ_SIZE, SQ_SIZE))
        s.set_alpha(50)
        s.fill(p.Color('green'))
        screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))


'''
Highlighting squares selected and possible moves
'''


def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r, c][0] == ('w' if gs.whiteToMove else 'b'):
            # gifhligt selected square
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color('blue'))
            screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s,
                                (SQ_SIZE * move.endCol, SQ_SIZE * move.endRow))


"""
Draws the pieces on the board using the current game state
"""


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r, c]
            if piece != "--":  # not empty
                screen.blit(IMAGES[piece],
                            p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


'''
Move animation
'''


def animateMove(move, screen, board, clock):
    global colors
    coords = []
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 5
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR * frame / frameCount,
                move.startCol + dC * frame / frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        # erase the piece moved from its ending square
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol * SQ_SIZE, move.endRow * SQ_SIZE,
                           SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        #draw captured piece onto rectangle
        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        #draw moving piece
        screen.blit(IMAGES[move.pieceMoved],
                    p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)


def drawText(screen, text):
    font = p.font.SysFont("Helvetica", 32, True, False)
    textObject = font.render(text, 0, p.Color('Black'))
    textlocation = p.Rect(0, 0, WIDTH, HEIGHT).move(
        WIDTH / 2 - textObject.get_width() / 2,
        HEIGHT / 2 - textObject.get_height() / 2)
    screen.blit(textObject, textlocation)
    textObject = font.render(text, 0, p.Color("gray"))
    screen.blit(textObject, textlocation.move(2, 2))


if __name__ == "__main__":
    main()

# STOP_WORD
