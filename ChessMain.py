# handle user interaction
import sys
import pygame as p
import ChessEngine
import MoveFinder
from constraint import *


def loadImages():
    pieces = ['wp', 'bp', 'wr', 'br', 'wn',
              'bn', 'wb', 'bb', 'wq', 'bq', 'wk', 'bk']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(
            'images/'+piece+'.png'), (SQ_SIZE, SQ_SIZE))


def loadLargeImage():
    pieces = ['wr', 'bn', 'wb', 'bq']
    for piece in pieces:
        LARGE_IMAGES[piece] = p.transform.scale(p.image.load(
            'images/'+piece+'.png'), (2*SQ_SIZE, 2*SQ_SIZE))


def main(mode, firstTurn, whiteLevel, blackLevel):
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color('white'))

    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    gameOver = False

    firstTurnForPlayer = firstTurn  # người chơi (hoặc AI chính) đi trước
    AgentLevel = blackLevel if firstTurn else whiteLevel
    combo = 5.0
    playerScore = agentScore = abs(MoveFinder.scoreBoard(gs, AgentLevel))
    upPlayerScore = upAgentScore = 0

    def estimate(nextScore, isAgent: bool):
        nonlocal combo, agentScore, playerScore, upPlayerScore, upAgentScore
        if isAgent:
            upAgentScore = nextScore - agentScore
            agentScore = nextScore
            if upAgentScore > upPlayerScore:
                combo = min(combo + 0.2, 10)
            else:
                combo = max(combo - 0.2, 0)
        else:
            upPlayerScore = nextScore - playerScore
            playerScore = nextScore

    loadImages()
    loadLargeImage()

    running = True
    sqSelected = ()

    while running:
        if mode == 1 and not gameOver:
            radom_AI_turn = firstTurnForPlayer == gs.whiteToMove

            if radom_AI_turn:
                for e in p.event.get():
                    if e.type == p.QUIT:
                        running = False
                AImove = MoveFinder.findRandomMove(validMoves)
                if AImove.isPromote:
                    AImove.promoteTo = MoveFinder.findRandomPromote()
                gs.makeMove(AImove)
                print(AImove.getChessNotation())
                moveMade = True

            else:
                # AI xử lý
                AImove = MoveFinder.findBestMove(gs, validMoves, AgentLevel)
                if AImove is None:
                    AImove = MoveFinder.findRandomMove(validMoves)
                if AImove.isPromote:
                    AImove.promoteTo = MoveFinder.findRandomPromote('q')
                gs.makeMove(AImove)
                print(AImove.getChessNotation())
                moveMade = True
                estimate(abs(MoveFinder.scoreBoard(gs, AgentLevel)), True)

        elif mode == 0 and not gameOver:
            isWhiteTurn = gs.whiteToMove
            level = whiteLevel if isWhiteTurn else blackLevel

            for e in p.event.get():
                if e.type == p.QUIT:
                    running = False

            AImove = MoveFinder.findBestMove(gs, validMoves, level)
            if AImove is None:
                AImove = MoveFinder.findRandomMove(validMoves)
            if AImove.isPromote:
                AImove.promoteTo = MoveFinder.findRandomPromote('q')
            gs.makeMove(AImove)
            print(AImove.getChessNotation())
            moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs, validMoves, sqSelected)

        if len(validMoves) == 0:
            gameOver = True
            running = False
            if gs.checkMate:
                drawText(
                    screen, ('Black' if gs.whiteToMove else 'White') + ' wins!!!')
            elif gs.staleMate:
                drawText(screen, 'Draw!!!')
            if mode == 1:
                print('Level of AI Agent:', combo)

        clock.tick(MAX_FPS)
        p.display.flip()

        while gameOver:
            for e in p.event.get():
                if e.type == p.QUIT:
                    exit()


def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen)
    highlightSqSelected(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)


def drawBoard(screen):
    colors = [p.Color('white'), p.Color('gray')]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r+c) % 2]
            p.draw.rect(screen, color, p.Rect(
                c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != '--':
                screen.blit(IMAGES[piece], p.Rect(
                    c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPromoteSelection(p, screen):
    screen = p.display.set_mode((WIDTH, HEIGHT+2*SQ_SIZE))
    colors = [p.Color('white'), p.Color('black')]
    for c in range(int(DIMENSION/2)):
        color = colors[c % 2]
        p.draw.rect(screen, color, p.Rect(
            c*2*SQ_SIZE, DIMENSION*SQ_SIZE, 2*SQ_SIZE, 2*SQ_SIZE))
    screen.blit(LARGE_IMAGES['bq'], p.Rect(
        0, DIMENSION*SQ_SIZE, 2*SQ_SIZE, 2*SQ_SIZE))
    screen.blit(LARGE_IMAGES['wr'], p.Rect(
        2*SQ_SIZE, DIMENSION*SQ_SIZE, 2*SQ_SIZE, 2*SQ_SIZE))
    screen.blit(LARGE_IMAGES['bn'], p.Rect(
        4*SQ_SIZE, DIMENSION*SQ_SIZE, 2*SQ_SIZE, 2*SQ_SIZE))
    screen.blit(LARGE_IMAGES['wb'], p.Rect(
        6*SQ_SIZE, DIMENSION*SQ_SIZE, 2*SQ_SIZE, 2*SQ_SIZE))


def highlightSqSelected(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(80)
            s.fill(p.Color('blue'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))

            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))


def drawText(screen, text):
    font = p.font.SysFont('Helvitca', 32, True, False)
    textObj = font.render(text, 0, p.Color('black'))
    textLoc = p.Rect(0, 0, WIDTH, HEIGHT).move(
        WIDTH/2 - textObj.get_width()/2, HEIGHT/2 - textObj.get_height()/2)
    screen.blit(textObj, textLoc)
    print(text)


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python3 chessmain.py <mode: 0|1> <firstTurn: 0|1> <whiteLevel: 1-10> <blackLevel: 1-10>")
        sys.exit(1)

    mode = int(sys.argv[1])
    firstTurn = not bool(int(sys.argv[2]))
    whiteLevel = int(sys.argv[3])
    blackLevel = int(sys.argv[4])
    if whiteLevel > 5 or blackLevel > 5:
        print("Level must be from 1 - 5")
        sys.exit(1)
    main(mode, firstTurn, whiteLevel, blackLevel)
