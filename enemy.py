import pygame
from settings import *
from pygame.math import Vector2
import random

class Enemy(object):
    def __init__(self, app, pos, idx):
        self.app = app
        self.grid_pos = pos
        self.pix_pos = self.get_pix_pos()
        self.index = idx
        self.color = self.select_color()
        self.direction = Vector2(0, 0)

    def get_pix_pos(self):
        x = TOP_BOTTOM_SPACE // 2 + self.grid_pos.x * self.app.cell_width + self.app.cell_width // 2
        y =  TOP_BOTTOM_SPACE // 2 + self.grid_pos.y * self.app.cell_height + self.app.cell_height // 2
        return Vector2(x, y)

    def draw(self):
        pygame.draw.circle(self.app.screen, self.color, self.pix_pos, self.app.cell_width // 2 - 2, 0)
        self.move()

    def move(self):
        # if self.index == 0:
        self.direction = self.get_random_direction()
        if self.able_to_move() == True:
            self.grid_pos += self.direction
            self.pix_pos = self.get_pix_pos()
        
        if self.grid_pos == self.app.player.grid_pos:
            self.app.player.lives -= 1

            if self.app.player.lives == 0:
                self.app.state = 'game-over'
                return

            self.app.player.grid_pos = Vector2(13, 29)
            self.app.player.draw()
            pygame.time.delay(100)
                
        for _ in range(10000):
            pass

    def get_random_direction(self):
        return random.choice([UP, DOWN, LEFT, RIGHT])

    def able_to_move(self):
        if Vector2(self.grid_pos + self.direction) in self.app.walls:
            return False
        return True

    def select_color(self):
        if self.index == 0:
            return BLUE
        if self.index == 1:
            return PINK
        if self.index == 2:
            return ORANGE
        if self.index == 3:
            return RED

