# Handles the user input and game state information
import sys, os, time
import pygame as p
import ChessMain as CM

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

background = "./Chess/images/Bg/limusa-cat-playing-chess.gif"

screen = p.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))

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
end_button = Button('Quit', 200, 50,(270, 360), 6)
start_game = Button('Play', 200, 50,(270, 150), 4)
player_one = Button('Player 1', 200, 50,(270, 250), 4)
player_two = Button('Player 2', 200, 50,(270, 350), 4)

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

        end_button.draw()
        if end_button.is_clicked():
            running = False
            p.quit()
            sys.exit()

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
            time.sleep(.5)
            CM()

        clock.tick(MAX_FPS)
        p.display.flip()

if player_one.is_clicked():
    CM.player_one = True
    print("Player 1 is Human")
else:
    CM.player_one = False
    print("Player 1 is Computer")

if player_two.is_clicked():
    CM.player_two = True
    print("Player 2 is Human")
else:
    CM.player_two = False
    print("Player 2 is Computer")


def start_game_with_delay():
    time.sleep(.5)


if __name__ == "__main__":
    main()