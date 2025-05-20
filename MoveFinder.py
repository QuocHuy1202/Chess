from copy import deepcopy
import random

from constraint import *


def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]


def findRandomPromote(promoteTo=None):
    return ['q', 'n', 'r', 'b'][random.randint(0, 3)] if promoteTo is None else promoteTo


def scoreBoard(gs, level):
    if gs.checkMate:
        if gs.whiteToMove:
            return -CHECKMATE
        else:
            return CHECKMATE
    elif gs.staleMate:
        return STALEMATE
    pos_table = PIECE_POSITIONS_SCORE[level-1]
    piece_score = PIECESCORE[level-1]
    weight_s = WEIGHT_SCORE[level-1]
    score = 0
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            piecePositionScore = 0
            square = gs.board[row][col]
            if square == '--':
                continue
            if not gs.whiteToMove and square[0] == 'w':
                if square[1] == 'p':
                    piecePositionScore = pos_table['wp'][row][col] * \
                        weight_s['p']
                elif square[1] != 'k':
                    piecePositionScore = pos_table[square[1]
                                                   ][row][col] * weight_s[square[1]]
                score += piece_score[square[1]] + piecePositionScore
            elif gs.whiteToMove and square[0] == 'b':
                if square[1] == 'p':
                    piecePositionScore = pos_table['bp'][row][col] * \
                        weight_s['p']
                elif square[1] != 'k':
                    piecePositionScore = pos_table[square[1]
                                                   ][row][col] * weight_s[square[1]]
                score -= piece_score[square[1]] + piecePositionScore
    return score


def findBestMove(gs, validMoves, level):
    global nextMove
    nextMove = None
    random.shuffle(validMoves)
    max_depth = DEPTH[level-1]
    findMoveMinimax(gs, validMoves, max_depth, -CHECKMATE,
                    CHECKMATE, 1 if gs.whiteToMove else -1, max_depth)
    return nextMove


def findMoveMinimax(gs, validMoves, depth, alpha, beta, turn, level):
    global nextMove
    if depth == 0:
        return turn * scoreBoard(gs, level)

    maxScore = -CHECKMATE
    for move in validMoves:
        if move.isPromote:
            move.promoteTo = findRandomPromote('q')
        local_gs = deepcopy(gs)
        local_gs.makeMove(move)
        nextMoves = local_gs.getValidMoves()
        score = -findMoveMinimax(local_gs, nextMoves,
                                 depth-1, -beta, -alpha, -turn, level)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH[level-1]:
                nextMove = move

        if maxScore > alpha:
            alpha = maxScore
        if alpha >= beta:
            break

    return maxScore
