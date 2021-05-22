import pygame
from settings import *
from pygame.math import Vector2

class Player(object):
    def __init__(self, app, start_pos):
        self.app = app
        self.grid_pos = start_pos
        self.pix_pos = self.get_pix_pos()
        self.score = 0
        self.direction = Vector2(0, 0)

    def get_pix_pos(self):
        x = TOP_BOTTOM_SPACE // 2 + self.grid_pos.x * self.app.cell_width + self.app.cell_width // 2
        y =  TOP_BOTTOM_SPACE // 2 + self.grid_pos.y * self.app.cell_height + self.app.cell_height // 2
        return Vector2(x, y)

    def draw(self):
        if self.able_to_move():
            self.grid_pos += self.direction
            self.pix_pos = self.get_pix_pos()
        self.eat_coin()

        pygame.draw.circle(self.app.screen, YELLOW, self.pix_pos, self.app.cell_width // 2 - 2, 0)

    def move(self, direction):
        self.direction = direction

    def able_to_move(self):
        if Vector2(self.grid_pos + self.direction) in self.app.walls:
            return False
        else:
            return True  

    def eat_coin(self):
        if Vector2(self.grid_pos) in self.app.coins:
            self.app.coins.remove(Vector2(self.grid_pos))
            self.score += 1

    # player will keep on moving 
    # we will press the keys to only change direction 


    