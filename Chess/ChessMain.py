# Handles the user input and game state information

import pygame as p
from pygame import mixer
import ChessEngine, ChessAi
import sys, os

# Changes the title of the window and the programs image
p.display.set_caption('Chess')
mixer.init()

# Check the OS, because using backslashes in paths is not POSIX friendly, making it compatible with MacOS, and Linux
ImageWinPath = ".\Chess\images\chess.png"
ImageLinuxPath = "./Chess/images/chess.png"
ImageDirWin = ".\Chess\images\\"
ImageDirLinux = "./Chess/images/"

MusicWinPath = ".\Chess\Chess_Music.mp3"
MusicLinuxPath = "./Chess/Chess_Music.mp3"
#check if the game is being ran inside the Chess folder, so its compatible either way
if(os.getcwd().endswith("Chess") and os.getcwd().endswith("Chess/Chess") or os.getcwd().endswith("Chess\Chess")):
    ImageWinPath = ".\images\chess.png"
    ImageLinuxPath = "./images/chess.png"
    ImageDirWin = "images\\"
    ImageDirLinux = "./images/"

os=sys.platform
if(os == "win32"):
    p.display.set_icon(p.image.load(ImageWinPath))
    mixer.music.load(MusicWinPath)
elif(os == "cygwin"):
    p.display.set_icon(p.image.load(ImageLinuxPath))
    mixer.music.load(MusicWinPath)
else:
    p.display.set_icon(p.image.load(ImageLinuxPath))
    mixer.music.load(MusicLinuxPath)

WIDTH = HEIGHT = 500  # 500 is the best size for the window do to the size and reselution of the pieces
DIMENSION = 8  # dimensions of a chess board are 8x8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15  # For animation later on
IMAGES = {}

# Play Music
#mixer.music.play()

# Loading the images and will initialize a global dictionary of images.

def load_images():
    pieces = ["--","wp", "wN", "wB", "wR", "wQ", "wK", "bp", "bN", "bB", "bR", "bQ", "bK"]
    for piece in pieces:
        if(os == "win32"):
            IMAGES[piece] = p.transform.scale(p.image.load(ImageDirWin + piece + ".png"), (SQ_SIZE, SQ_SIZE))
        elif(os == "cygwin"):
            IMAGES[piece] = p.transform.scale(p.image.load(ImageDirWin + piece + ".png"), (SQ_SIZE, SQ_SIZE))
        else:
            IMAGES[piece] = p.transform.scale(p.image.load(ImageDirLinux + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    # Note: we can access an image by saying  'IMAGES['wp']'


# This will handle the user input and update the graphics

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("black"))
    gs = ChessEngine.GameState()

    valid_moves = gs.valid_moves()
    moveMade = False # The flag varuable for when the game state is changed or move is made

    animate = False # Falg variable for when we should animate a move

    load_images() # Only do this once, before the while loop.
    running = True

    sqSelected = () # On start no square will be selected, also keeps track of the user input (tuple: row, col)
    playerClicks = [] # Keep track of the player clicks (two tuples: [(6, 4), (4, 4)])

    gameOver = False

    playerOne = True # IF a person is playing white then the varuable will be true while if ai plays then false
    playerTwo = True # Same as a bove just for black

    while running:
        #Check to see if a human is playing
        isHumanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)

        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            # Mouse Input Handler
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and isHumanTurn:
                    location = p.mouse.get_pos() # This is the postion of the (x,y) location of the mouse
                
                    col = location[0] //SQ_SIZE
                    row = location[1] //SQ_SIZE

                    if sqSelected == (row, col): #  The user clicked the same square twice
                        sqSelected = () # deslected
                        playerClicks = [] # Clear the player clicks
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected) # Append for both first and secound clicks
                    
                    if len(playerClicks) == 2: # After the secound click
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        print(move.getChessNotation())

                        for i in range(len(valid_moves)):
                            if move == valid_moves[i]:
                                gs.make_move(valid_moves[i])
                                moveMade = True
                                animate = True
                                sqSelected = () # Reset the user clicks
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]

            # Key Handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_u: # Undos when 'u' is pressed
                    gs.undo_move()
                    moveMade = True
                    animate = False

                if e.key == p.K_r: # Reset the board when 'r' is pressed
                    gs = ChessEngine.GameState()
                    valid_moves = gs.valid_moves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = True
                    animate = False

        # The Ai move finder object
        if not gameOver and not isHumanTurn:
            AIMove = ChessAi.FindRandomMoce(valid_moves)
            gs.make_move(AIMove)
            moveMade = True
            animate = True

        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            valid_moves = gs.valid_moves()
            moveMade = False
            animate = False

        drawGameState(screen, gs, valid_moves, sqSelected)

        if gs.checkmate:
            gameOver = True

            if gs.whiteToMove:
                drawText(screen, 'Black wins by checkmate!')
            else:
                drawText(screen, 'White wins by checkmate!')
        elif gs.stalemate:
            gameOver = True
            drawText(screen, 'Stalemate')

        clock.tick(MAX_FPS)
        p.display.flip()


# Highlight the square selected on the board and the piece selected

def highlightSquares(screen, gs, valid_Moves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'): # sqSelected is a piece that can be moved
            #Highlight the sqSelected square
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100) #Transperancy value
            s.fill(p.Color('cyan'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            #Highlight moves from that square
            s.fill(p.Color('olivedrab1'))
            for move in valid_Moves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (SQ_SIZE*move.endCol, SQ_SIZE*move.endRow))

# Responsible for all the graphics within the current gamestate.

def drawGameState(screen, gs, valid_Moves, sqSelected):
    drawBoard(screen) # Draws the squares on the board
    highlightSquares(screen, gs, valid_Moves, sqSelected)
    drawPieces(screen, gs.board) # Draw the pieces on the board

# draw the squares on the board

def drawBoard(screen):
    global colors
    colors = [p.Color("lightyellow1"), p.Color("lightsalmon1")]

    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

# Draws the pieces on the board

def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != 0:  # not empty square
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

# Animations for the pieces
def animateMove(move, screen, board, clock):
    global colors
    coords = [] # List of the cords that the animation will move through
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    fPS = 5 # Frames to move one square
    frameCount = (abs(dR) + abs(dC)) * fPS

    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR * frame / frameCount, move.startCol + dC * frame / frameCount)

        drawBoard(screen)
        drawPieces(screen, board)

        # erase the piece moved from its ending square
        color = colors[(move.endRow + move.endCol) % 2]

        endSquare = p.Rect(move.endCol * SQ_SIZE, move.endRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)

        # Draw captuered piece ontp the rectangle
        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured], endSquare)

        # Draw moing piece
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)

def drawText(screen, text):
    font = p.font.SysFont("Poppin", 32, False, False)
    textObj = font.render(text, 0, p.Color('Gray'))
    textLoc = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - textObj.get_width() / 2, HEIGHT / 2 - textObj.get_height() / 2)
    screen.blit(textObj, textLoc)
    textObj = font.render(text, 0, p.Color('Black'))
    screen.blit(textObj, textLoc.move(2, 1))

if __name__ == "__main__":
    main()
