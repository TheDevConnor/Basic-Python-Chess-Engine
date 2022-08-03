# Handles the user input and game state information
import sys, os, time
import pygame as p
from pygame import mixer
import ChessEngine, ChessAi
from multiprocessing import Process, Queue

#_established = False
#print("established = " + str(_established))
BOARD_WIDTH = BOARD_HEIGHT = 500  # 500 is the best size for the window do to the size and reselution of the pieces
MOVE_LOG_PANEL_WIDTH = 250
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
DIMENSION = 8  # dimensions of a chess board are 8x8
SQ_SIZE = BOARD_HEIGHT // DIMENSION
MAX_FPS = 15  # For animation later on
IMAGES = {}
DEBUG_MODE = True
WIDTH = 750
HEIGHT = 500
    
# Changes the title of the window and the programs image
p.display.set_caption('Chess')
screen = p.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
# mixer.init()


global inChessDir
inChessDir = None

# Check the OS, because using backslashes in paths is not POSIX friendly, making it compatible with MacOS, and Linux
ImageWinPath = ".\Chess\images\chess.png"
ImageLinuxPath = "./Chess/images/chess.png"
ImageDirWin = ".\Chess\images\\"
ImageDirLinux = "./Chess/images/"

MusicWinPath = ".\Chess\Music\Sonar.mp3"
MusicLinuxPath = "./Chess/Music/Sonar.mp3"

ButtonImgLinux = "./Chess/images/Buttons/start.png"
start_button_img = p.image.load(ButtonImgLinux).convert_alpha()

PieceMovedPath = "./Chess/Music/PieceMoved.mp3"

background = "./Chess/images/Bg/bg.png"

InCheckPath = "./Chess/Music/inCheck.mp3"

#check if the game is being ran inside the Chess folder, so its compatible either way
if(os.getcwd().endswith("Chess") and os.getcwd().endswith("Chess/Chess") or os.getcwd().endswith("Chess\Chess")):
    inChessDir = True
    ImageWinPath = ".\images\chess.png"
    ImageLinuxPath = "./images/chess.png"
    ImageDirWin = "images\\"
    ImageDirLinux = "./images/"
else:
    inChessDir = False

os=sys.platform
if(os == "win32"):
    p.display.set_icon(p.image.load(ImageWinPath))
    # mixer.music.load(MusicWinPath)
elif(os == "cygwin"):
    p.display.set_icon(p.image.load(ImageLinuxPath))
    # mixer.music.load(MusicWinPath)
else:
    p.display.set_icon(p.image.load(ImageLinuxPath))
    # mixer.music.load(MusicLinuxPath)



# Play Music
# mixer.music.play(-1)
# Set Music volume and Sound effect volume
# mixer.music.set_volume(.05)

class Button():
    p.init()
    def __init__(self, text, width, height, pos, elevation):
        # Animate the button
        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.original_elevation = pos[1]

        # Top rectangle
        self.top_rect = p.Rect(pos, (width, height))
        self.top_color = '#65999A' 

        # Bottom rectangle
        self.bottom_rect = p.Rect(pos, (width, elevation))
        self.bottom_color = '#C0D5D6'

        # Render Text
        font = p.font.SysFont('Poppins', 32, False, False)
        self.text_surf = font.render(text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)
        

    def draw(self):
        # Elevation Animation
        self.top_rect.y = self.original_elevation - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center
        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation

        # Draw Bottom Rectangle
        p.draw.rect(screen, self.bottom_color, self.bottom_rect, border_radius=14)
        # Draw Top Rectangle
        p.draw.rect(screen, self.top_color, self.top_rect, border_radius=15)
        # Draw Text
        screen.blit(self.text_surf, self.text_rect)
        self.is_clicked()    

    def is_clicked(self):
        pressed = False
        is_mouse_pos = p.mouse.get_pos()

        if self.top_rect.collidepoint(is_mouse_pos):
            self.top_color = '#9A6665'
            if p.mouse.get_pressed()[0]:
                self.dynamic_elevation = 0
                pressed = True
            else:
                self.dynamic_elevation = self.elevation
                if pressed == True:
                    print("Button Pressed")
                    pressed = False
        else:
            self.dynamic_elevation = self.elevation
            self.top_color = '#65999A'
            pressed = False
        return pressed

# Create the nstance of the button
start_button = Button('Start', 200, 50,(270, 300), 6)
start_game = Button('Play', 200, 50,(270, 150), 4)
player_one = Button('Player 1', 200, 50,(270, 250), 4)
player_two = Button('Player 2', 200, 50,(270, 350), 4)

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

# Tells the user if they are playing as white or black
playerOne = True # IF a person is playing white then the varuable will be true while if ai plays then false
playerTwo = False # Same as above just for black

# This is the main menu for the game
def main():
    p.init()
    screen = p.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
    clock = p.time.Clock()

    font = p.font.SysFont('Poppins', 32, True, False)
    text_surf = font.render("Chess Engine in Python", False, (255, 255, 255))
    # text_with_ouline = add_outline_to_image(text_surf, 2, (0, 0, 0))
    # create a rectangular object for the
    # text surface object
    textRect = text_surf.get_rect()
    # set the center of the rectangular object.
    textRect.center = (WIDTH // 2, HEIGHT // 2)

    running = True

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

        bg = p.transform.scale(p.image.load(background), (WIDTH, HEIGHT))
        screen.blit(bg, (0, 0))
        screen.blit(text_surf, textRect)

        # Draw the buttons
        start_button.draw()
        if start_button.is_clicked():
            time.sleep(.5)
            Settings()

        clock.tick(MAX_FPS)
        p.display.flip()

def Settings():
    p.init()
    screen = p.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
    clock = p.time.Clock()

    running = True

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

        bg = p.transform.scale(p.image.load(background), (WIDTH, HEIGHT))
        screen.blit(bg, (0, 0))

        # Draw the buttons
        start_game.draw()
        player_one.draw()
        player_two.draw()
        if start_game.is_clicked():
            start_game_with_delay()

        clock.tick(MAX_FPS)
        p.display.flip()

def start_game_with_delay():
    time.sleep(.5)
    Chess()

# This will handle the user input and update the graphics
def Chess():
    p.init()
    clock = p.time.Clock()
    screen.fill(p.Color("black"))
    gs = ChessEngine.GameState()

    valid_moves = gs.valid_moves()
    moveMade = False # The flag varuable for when the game state is changed or move is made

    animate = False # Falg variable for when we should animate a move

    moveLogFont = p.font.SysFont("Poppin", 20, False, False)

    load_images() # Only do this once, before the while loop.
    running = True

    sqSelected = () # On start no square will be selected, also keeps track of the user input (tuple: row, col)
    playerClicks = [] # Keep track of the player clicks (two tuples: [(6, 4), (4, 4)])

    # For the AI to play
    AI_thinking = False
    move_find_process = None

    gameOver = False

    while running:
        #Check to see if a human is playing
        isHumanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)

        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            # Mouse Input Handler
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver:
                    location = p.mouse.get_pos() # This is the postion of the (x,y) location of the mouse
                
                    col = location[0] //SQ_SIZE
                    row = location[1] //SQ_SIZE

                    if sqSelected == (row, col) or col >= 8: #  The user clicked the same square twice
                        sqSelected = () # deslected
                        playerClicks = [] # Clear the player clicks
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected) # Append for both first and secound clicks
                    
                    if len(playerClicks) == 2 and isHumanTurn: # After the secound click
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        #print(move.getChessNotation())

                        for i in range(len(valid_moves)):
                            if move == valid_moves[i]:
                                gs.make_move(valid_moves[i])
                                moveMade = True 
                                animate = True
                                # mixer.Sound(PieceMovedPath).play()
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
                    gameOver = False

                if e.key == p.K_r: # Reset the board when 'r' is pressed
                    gs = ChessEngine.GameState()
                    valid_moves = gs.valid_moves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
                    gameOver = False

        # The Ai move finder object
        if not gameOver and not isHumanTurn:
            AIMove = ChessAi.find_best_move(gs, valid_moves)
            if AIMove is None:
                AIMove = ChessAi.find_random_move(valid_moves)
            gs.make_move(AIMove)
            moveMade = True
            animate = True
            # mixer.Sound(PieceMovedPath).play()

        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            valid_moves = gs.valid_moves()
            moveMade = True
            animate = False

        drawGameState(screen, gs, valid_moves, sqSelected, moveLogFont)

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

def drawGameState(screen, gs, valid_Moves, sqSelected, moveLogFont):
    drawBoard(screen) # Draws the squares on the board
    highlightSquares(screen, gs, valid_Moves, sqSelected)
    drawPieces(screen, gs.board) # Draw the pieces on the board
    draw_move_log(screen, gs, moveLogFont)

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
    fPS = 2 # Frames to move one square
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
            if move.isEnpassantMove:
                enPassantRow = (move.endRow + 1) if move.pieceCaptured[0] == 'b' else (move.endRow - 1)
                endSquare = p.Rect(move.endCol * SQ_SIZE, enPassantRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            screen.blit(IMAGES[move.pieceCaptured], endSquare)


        # Draw moing piece
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)

def draw_move_log(screen, gs: ChessEngine.GameState, font):
    move_log_rect = p.Rect(BOARD_WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
    p.draw.rect(screen, p.Color("black"), move_log_rect)

    move_log = gs.moveLog
    move_texts = []

    for i in range(0, len(move_log), 2):
        move_string = str(i//2 + 1) + ". " + str(move_log[i]) + " "
        if i+1 < len(move_log):
            move_string += str(move_log[i+1]) + " "
        move_texts.append(move_string)

    moves_per_row = 2
    padding = 5
    line_spacing = 10
    text_y = padding

    for i in range(0, len(move_texts), moves_per_row):
        text = " "
        for j in range(moves_per_row):
            if i + j < len(move_texts):
                text += move_texts[i + j]
        textObj = font.render(text, True, p.Color('white'))
        textLoc = move_log_rect.move(padding, text_y)
        screen.blit(textObj, textLoc)
        text_y += textObj.get_height() + line_spacing


def drawText(screen, text):
    font = p.font.SysFont("Poppin", 32, False, False)
    textObj = font.render(text, 0, p.Color('Gray'))
    textLoc = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH/2 - textObj.get_width() / 2, BOARD_HEIGHT / 2 - textObj.get_height() / 2)
    screen.blit(textObj, textLoc)
    textObj = font.render(text, 0, p.Color('Black'))
    screen.blit(textObj, textLoc.move(2, 1))

# This main is a pain in our ass
if __name__ == "__main__":
    Chess()