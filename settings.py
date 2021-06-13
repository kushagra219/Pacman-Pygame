import sys
import os
from pygame.math import Vector2

def resource_path(relative_path):
    try: 
        base_path = sys._MEIPASS
        base_path = base_path.replace("\\", "/")
    except:
        base_path = os.path.abspath('.')
    
    return base_path + '/' + relative_path

# SCREEN SETTINGS
SCREEN_WIDTH, SCREEN_HEIGHT = 610, 670
TOP_BOTTOM_SPACE = 50
MAZE_WIDTH, MAZE_HEIGHT = SCREEN_WIDTH - TOP_BOTTOM_SPACE, SCREEN_HEIGHT - TOP_BOTTOM_SPACE

# FPS
FPS = 10

# ROWS AND COLS
ROWS = 31
COLS = 28 

# UP, DOWN, LEFT, RIGHT
UP = Vector2(0, -1)
DOWN = Vector2(0, 1)
LEFT = Vector2(-1, 0)
RIGHT = Vector2(1, 0)

# COLOR SETTINGS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
SILVER = (192, 192, 192)
GREY = (128, 128, 128)
MAROON = (128, 0, 0)
OLIVE = (128, 128, 0)
DARK_GREEN = (0, 128, 0)
PURPLE = (128, 0, 128)
TEAL = (0, 128, 128)
NAVY = (0, 0, 128)
ORANGE_RED = (255,69,0)
ORANGE = (255,165,0)
GOLD = (255,215,0)
GRAY_DARK = (104, 107, 106)
GRAY_LIGHT = (161, 166, 165)
PINK = (225, 150, 150)

# FONT SETTINGS
DEFAULT_FONT = 'arial black'
DEFAULT_SIZE = 18
