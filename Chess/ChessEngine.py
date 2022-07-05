# Storing all the information about the current state of the chess game. As well
# as determine the valid moves as well
# keeping take of the move logs

class GameState():
    def __init__(self):
        # Board is a 8x8 two dimensional plane

        # The plane has a list of characters the first character represents the color while the color 'b' or 'w'
        # While the secound character represents the type of the piece 'K' 'Q' 'B' 'N' 'R' or 'p'
        # "--" represents an empty space with no pieces
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]

        self.moveFunctions = {"p": self.getPawnMove, "R": self.getRookMove, "N": self.getKnightMove,
                              "B": self.getBishopMove, "Q": self.getQueenMove, "K": self.getKingMove}

        self.whiteToMove = True
        self.moveLog = []

        # Keeps the laction of the kings
        self.whiteKingLoct = (7, 4)
        self.blackKingLoct = (0, 4)

        #Checks for pins checks and as well as enpassant
        self.inCheck = False
        self.pins = []
        self.checks = []
        self.empassantPossible = () # coordinates for the square where it is possable

        # CheckMate and stalemate
        self.checkmate = False
        self.stalemate = False

        # Castleing
        self.whiteCastleKingSide = True
        self.whiteCastleQueenSide = True

        self.blackCastleKingSide = True
        self.blackCaskteQueenSide = True

        self.castleRightLog = [CastleRights(self.whiteCastleKingSide, self.whiteCastleQueenSide,
                                            self.blackCastleKingSide, self.blackCaskteQueenSide)]

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) # Log move so we can undo later
        self.whiteToMove = not self.whiteToMove #swap players
        
        # Update the kings location if moved
        if move.pieceMoved == "wK":
            self.whiteKingLoct = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            self.blackKingLoct = (move.endRow, move.endCol)

        # If pawn moves twice, next move can be captured enpassant
        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
            self.empassantPossible = ((move.endRow + move.startRow) // 2, move.endCol)
        else:
            self.empassantPossible = ()
        
        # If enpassant move, must update the board to captures the pawn
        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = "--"\

        # Pawn Promotion
        if move.pawnPromotion:
            promotedPiece = input("Promote to Q, R, B, or N:") 
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + promotedPiece

        # Caslt Move
        if move.castle:
            if move.endCol - move.startCol == 2: # Kingside Castle
                self.board[move.endRow][move.endCol-1] = self.board[move.endRow][move.endCol+1] # moves the rook
                self.board[move.endRow][move.endCol+1] = '--' # erease old rook
            else: # Queen side castle
                self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-2] # moves the rook
                self.board[move.endRow][move.endCol-2] = '--'

        # Updating the castling rights -- Whenever it is a rook or a king move\
        self.updateCastleRights(move)
        self.castleRightLog.append(CastleRights(self.whiteCastleKingSide, self.blackCastleKingSide,
                                                self.whiteCastleQueenSide, self.blackCaskteQueenSide))

        

    # Undo your last move
    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove # switch turns back

            # Update the kings location if needed
            if move.pieceMoved == "wK":
                self.whiteKingLoct = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.blackKingLoct = (move.startRow, move.startCol)

            #Undo EnpassantMove
            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol] = "--" # Leave the landing square blank
                self.board[move.startRow][move.endCol] = move.pieceCaptured
                self.empassantPossible = (move.endRow, move.endCol)
            # undo a 2 square pawn advance
            if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
                self.empassantPossible = ()

            #Undo Castling Rights
            self.castleRightLog.pop() # get rid of the new castlke rights form the move we are undoing
            CastleRights = self.castleRightLog[-1] # setting the new castle rights

            self.whiteCastleKingSide = CastleRights.wks
            self.whiteCastleQueenSide = CastleRights.wqs

            self.blackCastleKingSide = CastleRights.bks
            self.blackCaskteQueenSide = CastleRights.bqs

            # Undo the castle move
            if move.castle:
                if move.endCol - move.startCol == 2: # kingside
                    self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-1]
                    self.board[move.endRow][move.endCol-1] = '--'
                else: # Queen Side castle
                    self.board[move.endRow][move.endCol-2] = self.board[move.endRow][move.endCol+1]
                    self.board[move.endRow][move.endCol+1] = '--'

    # All moves considering a check
    def validMoves(self):
        moves = []

        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()

        if self.whiteToMove:
            kingRow = self.whiteKingLoct[0]
            kingCol = self.whiteKingLoct[1]
        else:
            kingRow = self.blackKingLoct[0]
            kingCol = self.blackKingLoct[1]

        if self.inCheck:
            if len(self.checks) == 1:
                moves = self.allPossableMoves()

                check = self.checks[0]
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol]
                validSquares = []

                if pieceChecking[1] == 'N':
                    validSquares = [(checkRow, checkCol)]
                else:
                    for i in range(1, 8):
                        validSquare = (kingRow + check[2] * i, kingCol + check[3] * i)
                        validSquares.append(validSquare)

                        if validSquare[0] == checkRow and validSquare[1] == checkCol:
                            break
                for i in range(len(moves) -1, -1, -1):
                    if moves[i].pieceMoved[1] != 'K':
                        if not (moves[i].endRow, moves[i].endCol) in validSquares:
                            moves.remove(moves[i])
            else:
                self.getKingMove(kingRow, kingCol, moves)
        else:
            moves = self.allPossableMoves()
        
        if len(moves) == 0:
            if self.inCheck:
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.inCheck = False
            self.stalemate = False

        return moves

    #All moves not considering a check
    def allPossableMoves(self):
        moves = []
        for r in range(len(self.board)): # the number of rows
            for c in range(len(self.board[r])): # the number of cols
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves) # calls the correct move function based on move type
        return moves

    # Get the pawn moves
    def getPawnMove(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) -1, -1, -1):
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

        if self.board[r + moveAmount][c] == "--": # 1 square move
            if not piecePinned or pinDirection == (moveAmount, 0):
                if r + moveAmount == backRow: # if the piece gets to the back rank
                    pawnPromotion = True
                moves.append(Move((r, c), (r + moveAmount, c), self.board, pawnPromotion = pawnPromotion))
                if r == startRow and self.board[r + 2 * moveAmount][c] == "--": # 2 square move
                    moves.append(Move((r, c), (r + 2 * moveAmount, c), self.board))
        if c-1 >= 0: # Capture to the left
            if not piecePinned or pinDirection == (moveAmount, -1):
                if self.board[r + moveAmount][c - 1][0] == enemyColor:
                    if r + moveAmount == backRow: # if the piece gets to the back row and promots
                        pawnPromotion = True
                    moves.append(Move((r, c), (r + moveAmount, c-1), self.board, pawnPromotion = pawnPromotion))
                if (r + moveAmount, c - 1) == self.empassantPossible:
                    moves.append(Move((r, c), (r + moveAmount, c-1), self.board, isEnpassantMove = True))
        if c+1 <= 7: # Capture to the right
            if not piecePinned or pinDirection == (moveAmount, 1):
                if self.board[r + moveAmount][c + 1][0] == enemyColor:
                    if r + moveAmount == backRow: # if the piece gets to the back row and promots
                        pawnPromotion = True
                    moves.append(Move((r, c), (r + moveAmount, c+1), self.board, pawnPromotion = pawnPromotion))
                if (r + moveAmount, c + 1) == self.empassantPossible:
                    moves.append(Move((r, c), (r + moveAmount, c+1), self.board, isEnpassantMove = True))

    #get the rook moves 
    def getRookMove(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) -1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][1] != 'Q':
                    self.pins.remove(self.pins[i])
                break

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemyColor = 'b' if self.whiteToMove else 'w'
            
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i

                if 0 <= endRow < 8 and 0 <= endCol < 8: # on the board
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor: # enemy piece is valid
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break
                        else: # friendly piece invalid
                            break
                else: # off board
                    break

    #get the knight moves 
    def getKnightMove(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) -1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                self.pins.remove(self.pins[i])
                break

        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = 'w' if self.whiteToMove else 'b'

        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]

            if 0 <= endRow < 8 and 0 <= endCol < 8: # on the board
                if not piecePinned:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != allyColor: # not an ally piece (empty or enemy piece)
                        moves.append(Move((r, c), (endRow, endCol), self.board))

    #get the bishop moves 
    def getBishopMove(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) -1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemyColor = 'b' if self.whiteToMove else 'w'

        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                
                if 0 <= endRow < 8 and 0 <= endCol < 8: # on the board
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor: # enemy piece is valid
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break
                        else: # friendly piece invalid
                            break
                else: # off board
                    break

    #get the Queen moves 
    def getQueenMove(self, r, c, moves):
        self.getBishopMove(r, c, moves)
        self.getRookMove(r, c, moves)

    #get the king moves 
    def getKingMove(self, r, c, moves):
        rowMoves = (-1, -1, -1, 0, 0, 1, 1, 1)
        colMoves = (-1, 0, 1, -1, 1, -1, 0, 1)
        allyColor = 'w' if self.whiteToMove else 'b'

        for i in range(8):
            endRow = r + rowMoves[i]
            endCol = c + colMoves[i]

            if 0 <= endRow < 8 and 0 <= endCol < 8: # on the board
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor: # not an ally piece (empty or enemy piece)
                    if allyColor == 'w': # place king on the end square and check for checks
                        self.whiteKingLoct = (endRow, endCol)
                    else:
                        self.blackKingLoct = (endRow, endCol)
                    inCheck, pins, checks = self.checkForPinsAndChecks()
                    if not inCheck:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    if allyColor == 'w':
                        self.whiteKingLoct = (r, c)
                    else:
                        self.blackKingLoct = (r, c)

        self.getCastleMoves(r, c, moves, allyColor)

    # Generate the valid castlemoves
    def getCastleMoves(self, r, c, moves, allyColor):
        inCheck = self.squareUnderAttack(r, c, allyColor)
        if inCheck:
            print("oof")
            return

        if (self.whiteToMove and self.whiteCastleKingSide) or (not self.whiteToMove and self.blackCastleKingSide):
            self.getKingSideCastle(r, c, moves, allyColor)
        if (self.whiteToMove and self.whiteCastleQueenSide) or (not self.whiteToMove and self.blackCaskteQueenSide):
            self.getQueenSideCastle(r, c, moves, allyColor)

    def getKingSideCastle(self, r, c, moves, allyColor):
        if self.board[r][c+1] == "--" and self.board[r][c+2] == "--" and \
            not self.squareUnderAttack(r, c+1, allyColor) and not self.squareUnderAttack(r, c+2, allyColor):
                moves.append(Move((r, c), (r, c+2), self.board, castle=True))

    def getQueenSideCastle(self, r, c, moves, allyColor):
        if self.board[r][c-1] == "--" and self.board[r][c-2] == "--" and self.board[r][c-3] == "--" and \
            not self.squareUnderAttack(r, c-1, allyColor) and not self.squareUnderAttack(r, c-2, allyColor):
                moves.append(Move((r, c), (r, c-2), self.board, castle=True))

    def squareUnderAttack(self, r, c, allyColor):
        enemyColor = 'w' if allyColor == 'b' else 'b'
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            d = directions[j]
            for i in range(1, 8):
                    endRow = r + d[0] * i
                    endCol = c + d[1] * i

                    if 0 <= endRow < 8 and 0 <= endCol < 8:
                        endPiece = self.board[endRow][endCol]

                        if endPiece[0] == allyColor:
                            break
                        elif endPiece[0] == enemyColor:
                            type = endPiece[1]

                            if (0 <= j <= 3 and type == 'R') or \
                                    (4 <= j <= 7 and type == 'B') or \
                                    (i == 1 and type == 'p' and (
                                        (enemyColor == 'w' and 6 <= j <= 7) or (enemyColor == 'b' and 4 <= j <= 5))) or \
                                    (type == 'Q') or (i == 1 and type == 'K'):
                                return True
                            else: # Enemy piece not applying check
                                break
                    else:
                        break
               # Check for knight checks
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]

            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == 'N': # The enemy knight is attacking the king
                    return True
        return False

    def checkForPinsAndChecks(self):
        pins = []
        checks = []
        inCheck = False

        if self.whiteToMove:
            enemyColor = "b"
            allyColor = "w"
            startRow = self.whiteKingLoct[0]
            startCol = self.whiteKingLoct[1]
        else:
            enemyColor = "w"
            allyColor = "b"
            startRow = self.blackKingLoct[0]
            startCol = self.blackKingLoct[1]

            #Check outward from king for pins and checks, keep track of the pins
            directions = ((-1, 0), (0, -1), (1, 0), (0, 1),(-1, -1), (-1, 1), (1, -1), (1, 1))

            for j in range(len(directions)):
                d = directions[j]
                possiblePin = ()
                for i in range(1, 8):
                    endRow = startRow + d[0] * i
                    endCol = startCol + d[1] * i

                    if 0 <= endRow < 8 and 0 <= endCol < 8:
                        endPiece = self.board[endRow][endCol]

                        if endPiece[0] == allyColor and endPiece[1] != 'K':
                            if possiblePin == (): # 1st allied piece could be pinned
                                possiblePin = (endRow, endCol, d[0], d[1])
                            else: # 2nd allied piece, so no pin or check possible in this direction
                                break
                        elif endPiece[0] == enemyColor:
                            type = endPiece[1]

                            if (0 <= j <= 3 and type == 'R') or \
                                    (4 <= j <= 7 and type == 'B') or \
                                    (i == 1 and type == 'p' and ((enemyColor == 'w' and 6 <= j <= 7) or (enemyColor == 'b' and 4 <= j <= 5))) or \
                                    (type == 'Q') or (i == 1 and type == 'K'):
                                if possiblePin == (): # No piece blocking check
                                    inCheck = True
                                    checks.append((endRow, endCol, d[0], d[1]))
                                    break
                                else: #piece is blocking so pin
                                    pins.append(possiblePin)
                                    break
                            else: # Enemy piece not applying check
                                break
                    else: 
                        break # off the board

        # Check for knight checks
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knightMoves:
            endRow = startRow + m[0]
            endCol = startCol + m[1]

            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == 'N': # The enemy knight is attacking the king
                    inCheck = True
                    checks.append((endRow, endCol, m[0], m[1]))
        return inCheck, pins, checks

    def updateCastleRights(self, move):
        if move.pieceMoved == 'wk':
            self.whiteCastleQueenSide = False
            self.whiteCastleKingSide = False
        elif move.pieceMoved == 'bk':
            self.blackCaskteQueenSide = False
            self.blackCastleKingSide = False

        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startCol == 7:
                    self.whiteCastleKingSide = False
                elif move.startCol == 0:
                    self.whiteCastleQueenSide = False
        
        elif move.pieceMoved == 'bR':
            if move.startRow == 0:
                if move.startCol == 7:
                    self.blackCastleKingSide = False
                elif move.startCol == 0:
                    self.blackCaskteQueenSide = False

class CastleRights():
    def __init__(self, wks, bks, wqs, bqs):
        # White kings side castle
        self.wks = wks
        self.wqs = wqs

        # Black kings side castle
        self.bks = bks
        self.bqs = bqs

class Move():
    # Map the keys to a value
    # key : value

    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                  "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}

    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}


    def __init__(self, startSq, endSq, board, isEnpassantMove = False, pawnPromotion = False, castle = False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]

        self.endRow = endSq[0]
        self.endCol = endSq[1]

        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]

        # Pawn Promotion
        self.pawnPromotion = pawnPromotion
        #Enpassant
        self.isEnpassantMove = isEnpassantMove
        if isEnpassantMove:
            self.pieceCaptured = 'bp' if self.pieceMoved == 'wp' else 'wp'

        #Castling
        self.castle = castle

        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    # Overriding the equals method
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]