import pygame
from settings import *
from pygame.math import Vector2

player_img = pygame.image.load('assets/pacman-player.png')
player_shrink_img = pygame.transform.scale(player_img, (18, 18))

class Player(object):
    def __init__(self, app, start_pos):
        self.app = app
        self.image = player_shrink_img
        self.grid_pos = start_pos
        self.pix_pos = self.get_pix_pos()
        self.score = 0
        self.direction = Vector2(0, 0)
        self.lives = 3

    def get_pix_pos(self):
        x = TOP_BOTTOM_SPACE // 2 + self.grid_pos.x * self.app.cell_width   
        y =  TOP_BOTTOM_SPACE // 2 + self.grid_pos.y * self.app.cell_height 
        return Vector2(x, y)

    # def get_grid_pos(self):
    #     x = (self.pix_pos[0]- TOP_BOTTOM_SPACE +
    #                         self.app.cell_width // 2) // self.app.cell_width+1
    #     y = (self.pix_pos[1]- TOP_BOTTOM_SPACE +
    #                         self.app.cell_height//2) // self.app.cell_height+1
    #     return Vector2(x, y)

    def draw(self):
        if self.able_to_move():
            self.grid_pos += self.direction 
            self.pix_pos = self.get_pix_pos()
        self.eat_coin()

        self.app.screen.blit(self.image, self.pix_pos)
        # pygame.draw.circle(self.app.screen, YELLOW, self.pix_pos, self.app.cell_width // 2 - 2, 0)

        # Drawing Player Lives
        self.app.draw_text("Lives - ", self.app.screen, DEFAULT_FONT, DEFAULT_SIZE, WHITE, [25, SCREEN_HEIGHT - 28])
        for x in range(self.lives):
            self.app.screen.blit(player_shrink_img, (100 + 22 * x, SCREEN_HEIGHT - 22))
            # pygame.draw.circle(self.app.screen, YELLOW, (105 + 20 * x, SCREEN_HEIGHT - 15), 7)

    def move(self, direction):
        if direction == RIGHT:
            self.image = pygame.transform.rotate(player_shrink_img, 0)
        elif direction == LEFT:
            self.image = pygame.transform.rotate(player_shrink_img, 180)
        elif direction == UP:
            self.image = pygame.transform.rotate(player_shrink_img, 90)
        else:
            self.image = pygame.transform.rotate(player_shrink_img, -90)
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
            if self.score > self.app.high_score:
                self.app.high_score = self.score
                with open('high_score.txt', 'w') as file:
                    file.write(f"HIGHSCORE = {self.app.high_score}")

    # player will keep on moving 
    # we will press the keys to only change direction 

    


    