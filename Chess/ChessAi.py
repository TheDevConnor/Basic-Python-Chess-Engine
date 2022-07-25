import random

piece_score = {"K": 0, "Q": 10, "R": 5, "B": 3, "N": 3, "p": 1}
checkmate = 1000
stalemate = 0

def find_random_move(validMoves):
    return random.choice(validMoves)

def find_best_move(gs, validMoves):
    turn_multiplier = 1 if gs.whiteToMove else -1

    opps_min_max_score = checkmate
    best_move = None

    random.shuffle(validMoves)

    for player_move in validMoves:
        gs.make_move(player_move)

        opps_move = gs.valid_moves()
        opps_min_max_score = -checkmate

        if gs.checkmate():
            opps_max_score = -checkmate
        elif gs.stalemate():
            opps_max_score = stalemate
        else:
            opps_max_score = -checkmate
            for opps_move in opps_move:
                gs.make_move(opps_move)
                gs.valid_moves()
                if gs.checkmate:
                    score = checkmate
                elif gs.stalemate:
                    score = stalemate
                else:
                    score = -turn_multiplier * board_material(gs.board)

                if score > opps_max_score:
                    opps_max_score = score
                gs.undo_move()
        if opps_max_score < opps_min_max_score:
            opps_min_max_score = opps_max_score
            best_move = player_move
        gs.undo_move()
    return best_move

def board_material(board):
    score = 0

    for row in board:
        for square in row:
            if square[0] == 'w':
                score += piece_score[square[1]]
            elif square[0] == 'b':
                score -= piece_score[square[1]]
    return score