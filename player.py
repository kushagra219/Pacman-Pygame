import pygame
from settings import *
from pygame.math import Vector2

class Player(object):
    def __init__(self, app, start_pos):
        self.app = app
        self.grid_pos = start_pos
        self.pix_pos = self.get_pix_pos()

    def get_pix_pos(self):
        x = TOP_BOTTOM_SPACE // 2 + self.grid_pos.x * self.app.cell_width + self.app.cell_width // 2
        y =  TOP_BOTTOM_SPACE // 2 + self.grid_pos.y * self.app.cell_height + self.app.cell_height // 2
        return Vector2(x, y)

    def draw(self):
        pygame.draw.circle(self.app.screen, YELLOW, self.pix_pos, self.app.cell_width // 2 - 2, 0)

    def move(self, direction):
        self.grid_pos += direction
        self.pix_pos = self.get_pix_pos()