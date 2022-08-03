import random
#from ChessEngine import Move, GameState

piece_score = {"K": 0, "Q": 10, "R": 5, "B": 3, "N": 3, "p": 1}

knight_score =  [[1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 2, 2, 2, 2, 2, 2, 1],
                 [1, 2, 3, 3, 3, 3, 2, 1],
                 [1, 2, 3, 4, 4, 3, 2, 1],
                 [1, 2, 3, 4, 4, 3, 2, 1],
                 [1, 2, 3, 3, 3, 3, 2, 1],
                 [1, 2, 2, 2, 2, 2, 2, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1]]

bishop_score = [[4, 3, 2, 1, 1, 2, 3, 4],
                [3, 4, 3, 2, 2, 3, 4, 3],
                [2, 3, 4, 3, 3, 4, 3, 2],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [2, 3, 4, 3, 3, 4, 3, 2],
                [3, 4, 3, 2, 2, 3, 4, 3],
                [4, 3, 2, 1, 1, 2, 3, 4]]

queen_score = [[1, 1, 1, 3, 1, 1, 1, 1],
               [1, 2, 3, 3, 3, 1, 1, 1],
               [1, 4, 3, 3, 3, 4, 2, 1],
               [1, 2, 3, 3, 3, 2, 2, 1],
               [1, 2, 3, 3, 3, 2, 2, 1],
               [1, 4, 3, 3, 3, 4, 2, 1],
               [1, 2, 3, 3, 3, 1, 1, 1],
               [1, 1, 1, 3, 1, 1, 1, 1]]

rook_score = [[4, 3, 4, 4, 4, 4, 3, 4],
              [4, 4, 4, 4, 4, 4, 4, 4],
              [1, 1, 2, 3, 3, 2, 1, 1],
              [1, 2, 3, 4, 4, 3, 2, 1],
              [1, 2, 3, 4, 4, 3, 2, 1],
              [1, 1, 2, 3, 3, 2, 1, 1],
              [4, 4, 4, 4, 4, 4, 4, 4],
              [4, 3, 4, 4, 4, 4, 3, 4]]

white_pawn_score = [[8, 8, 8, 8, 8, 8, 8, 8],
                    [8, 8, 8, 8, 8, 8, 8, 8],
                    [5, 6, 6, 7, 7, 6, 6, 5],
                    [2, 3, 3, 5, 5, 3, 3, 2],
                    [1, 1, 2, 3, 3, 2, 1, 1],
                    [1, 1, 1, 0, 0, 1, 1, 1],
                    [0, 0, 0, 0, 0, 0, 0, 0]]

black_pawn_score = [[0, 0, 0, 0, 0, 0, 0, 0],
                    [1, 1, 1, 0, 0, 1, 1, 1],
                    [1, 1, 2, 3, 3, 2, 1, 1],
                    [2, 3, 3, 5, 5, 3, 3, 2],
                    [5, 6, 6, 7, 7, 6, 6, 5],
                    [8, 8, 8, 8, 8, 8, 8, 8],
                    [8, 8, 8, 8, 8, 8, 8, 8]]

piece_postion_scores = {"N": knight_score, "B": bishop_score, "Q": queen_score, 
                        "R": rook_score, "wp": white_pawn_score, "bp": black_pawn_score}

checkmate = 1000
stalemate = 0
DEPTH = 3

def find_random_move(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]

def find_best_move(gs, validMoves):
    global next_move,counter
    next_move = None
    random.shuffle(validMoves)
    counter = 0
    find_best_move_nega_max_alpha_beta(gs, validMoves, DEPTH, -checkmate, checkmate, 1 if gs.whiteToMove else -1)
    # returnQueue.put(next_move)
    return next_move

def find_best_move_nega_max_alpha_beta(gs, validMoves, deth, alpha, beta, turn_multiplier):
    global next_move,counter
    counter += 1

    if deth == 0:
        return turn_multiplier * score_board(gs)

    max_score = -checkmate

    for move in validMoves:
        gs.make_move(move)

        next_moves = gs.valid_moves()

        score = -find_best_move_nega_max_alpha_beta(gs, next_moves, deth-1, -beta, -alpha, -turn_multiplier)

        if score > max_score:
            max_score = score
            if deth == DEPTH:
                next_move = move
                print(f"Move: {move}, Score: {score}, Counter: {counter}")
        gs.undo_move()

        if max_score > alpha:
            alpha = max_score
        if alpha >= beta:
            break
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

    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]
            if square != "--":
                # Score it positionally
                piece_postion_score = 0
                if square[1] != "K": # no postion table for the king
                    if square[1] == "p": # for the pawns
                        piece_postion_score = piece_postion_scores[square][row][col]
                    else: # for other pieces
                        piece_postion_score = piece_postion_scores[square[1]][row][col]

                if square[0] == 'w':
                    score += piece_score[square[1]] + piece_postion_score * .39
                elif square[0] == 'b':
                    score -= piece_score[square[1]] + piece_postion_score * .39
                
    return score
