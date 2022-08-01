import random
import threading

from ChessEngine import Move, GameState

piece_score = {"K": 0, "Q": 10, "R": 5, "B": 3, "N": 3, "p": 1}

knight_score =  [[1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 2, 2, 2, 2, 2, 2, 1],
                 [1, 2, 3, 3, 3, 3, 2, 1],
                 [1, 2, 3, 4, 4, 3, 2, 1],
                 [1, 2, 3, 4, 4, 3, 2, 1],
                 [1, 2, 3, 3, 3, 3, 2, 1],
                 [1, 2, 2, 2, 2, 2, 2, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1]]

piece_postion_scores = {"N": knight_score}

checkmate = 1000
stalemate = 0
DEPTH = 5

def find_random_move(validMoves: list[Move]) -> Move:
    return validMoves[random.randint(0, len(validMoves)-1)]

def find_best_move(gs: GameState, validMoves: list[Move]) -> Move | None:
    global counter
    random.shuffle(validMoves)

    counter = 0
    _, next_move = find_best_move_nega_max_alpha_beta(gs, validMoves, DEPTH, 1 if gs.whiteToMove else 1, -checkmate, checkmate)
    print(counter)
    return next_move

def find_best_move_nega_max_alpha_beta(gs: GameState, validMoves: list[Move], deth: int, turn_multiplier: int, alpha: int, beta: int):
    global counter
    counter += 1

    next_move = None

    if deth == 0:
        return turn_multiplier * score_board(gs), None

    max_score = -checkmate
    for move in validMoves:
        gs.make_move(move)
        a, _ = find_best_move_nega_max_alpha_beta(gs, gs.valid_moves(), deth-1, -beta, -alpha, -turn_multiplier)
        score = -a
        if score > max_score:
            max_score = score
            next_move = move
        gs.undo_move()
        if max_score > alpha:
            alpha = max_score
        if alpha >= beta:
            break
    return max_score, next_move

def score_board(gs: GameState):
    if gs.checkmate:
        if gs.whiteToMove:
            return -checkmate # Black wins
        else:
            return checkmate # White wins
    elif gs.stalemate:
        return stalemate

    score = 0

    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]
            if square != "--":
                # Score it positionally
                piece_postion_score = 0
                if square[1] == "N":
                    piece_postion_score = piece_postion_scores["N"][row][col]



                if square[0] == 'w':
                    score += piece_score[square[1]] + piece_postion_score
                elif square[0] == 'b':
                    score -= piece_score[square[1]] + piece_postion_score
    return score

th = threading.Thread(target=find_best_move_nega_max_alpha_beta, args=())
th.start()
