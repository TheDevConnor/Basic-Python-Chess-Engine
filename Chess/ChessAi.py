import random

piece_score = {"K": 0, "Q": 10, "R": 5, "B": 3, "N": 3, "p": 1}
checkmate = 1000
stalemate = 0
_depth = 3

def find_random_move(validMoves):
    return random.choice(validMoves)

def find_best_move(gs, validMoves):
    global next_move
    next_move = None
    find_best_move_nega_max(gs, validMoves, _depth, 1 if gs.whiteToMove else -1)
    return next_move

def find_best_move_nega_max(gs, validMoves, deth, turn_multiplier):
    global next_move
    if deth == 0:
        return turn_multiplier * score_board(gs)

    max_score = -checkmate
    for move in validMoves:
        gs.make_move(move)
        next_move = gs.valid_moves()
        score = -find_best_move_nega_max(gs, next_move, deth-1, -turn_multiplier)
        if score > max_score:
            max_score = score
            if deth == _depth:
                next_move = move
        gs.undo_move()
    return max_score

def score_board(gs):
    if gs.checkmate:
        if gs.whiteToMove:
            return -checkmate # Black wins
        else:
            return checkmate # White wins
    elif gs.stalemate:
        return stalemate

    score = 0

    for row in gs.board:
        for square in row:
            if square[0] == 'w':
                score += piece_score[square[1]]
            elif square[0] == 'b':
                score -= piece_score[square[1]]
    return score

def board_material(board):
    score = 0

    for row in board:
        for square in row:
            if square[0] == 'w':
                score += piece_score[square[1]]
            elif square[0] == 'b':
                score -= piece_score[square[1]]
    return score 