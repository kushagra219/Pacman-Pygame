import pygame
import time
pygame.mixer.init()
from settings import *
from pygame.math import Vector2

player_img = pygame.image.load('assets/pacman-player.png')
player_shrink_img = pygame.transform.scale(player_img, (18, 18))
chomp_sound = pygame.mixer.Sound('assets/pacman_chomp.wav')
chomp_sound.set_volume(0.5)
enemy_intermission_img = pygame.transform.scale(pygame.image.load('assets/enemy_intermission.jpg'), (18, 18))

blue_ghost_img = pygame.image.load('assets/pacman-blue-ghost.jpg')
pink_ghost_img = pygame.image.load('assets/pacman-pink-ghost.jpg')
orange_ghost_img = pygame.image.load('assets/pacman-orange-ghost.jpg')
red_ghost_img = pygame.image.load('assets/pacman-red-ghost.jpg')

class Player(object):
    def __init__(self, app, start_pos):
        self.app = app
        self.image = player_shrink_img
        self.grid_pos = start_pos
        self.pix_pos = self.get_pix_pos()
        self.score = 0
        self.current_direction = Vector2(0, 0)
        self.stored_direction = Vector2(0, 0)
        self.lives = 3
        self.speed = 20
        self.intermission_start_time = None

    # finding pix_pos from grid_pos
    def get_pix_pos(self):
        x = TOP_BOTTOM_SPACE // 2 + self.grid_pos.x * self.app.cell_width   
        y =  TOP_BOTTOM_SPACE // 2 + self.grid_pos.y * self.app.cell_height 
        return Vector2(x, y)

    # finding grid_pos from pix_pos
    def get_grid_pos(self):
        x = (self.pix_pos.x - TOP_BOTTOM_SPACE // 2)  \
            // self.app.cell_width
        y = (self.pix_pos.y - TOP_BOTTOM_SPACE // 2)  \
            // self.app.cell_height
        return Vector2(x, y)

    def draw(self):
        if self.time_to_turn():
            self.current_direction = self.stored_direction

        if self.able_to_move():
            self.pix_pos += self.current_direction * self.speed
            self.grid_pos = self.get_grid_pos()
        self.rotate()

        self.eat_coin()
        self.eat_pellet()
        if self.app.intermission == True:
            if (time.time() - self.intermission_start_time) >= 10:
                print("end intermission")
                self.intermission_start_time = None
                self.app.intermission = False
                self.change_enemy_images_back()
                self.app.play_play_music()

        self.app.screen.blit(self.image, 
        (TOP_BOTTOM_SPACE // 2 + self.grid_pos.x * self.app.cell_width, 
        TOP_BOTTOM_SPACE // 2 + self.grid_pos.y * self.app.cell_height))
        # pygame.draw.circle(self.app.screen, YELLOW, self.pix_pos, self.app.cell_width // 2 - 2, 0)

        # Drawing Player Lives
        self.app.draw_text("Lives - ", self.app.screen, DEFAULT_FONT, DEFAULT_SIZE, WHITE, [25, SCREEN_HEIGHT - 28])
        for x in range(self.lives):
            self.app.screen.blit(player_shrink_img, (100 + 22 * x, SCREEN_HEIGHT - 22))
            # pygame.draw.circle(self.app.screen, YELLOW, (105 + 20 * x, SCREEN_HEIGHT - 15), 7)
    
    def time_to_turn(self):
        if self.stored_direction == LEFT:
            if self.grid_pos + LEFT not in self.app.walls:
                return True

        if self.stored_direction == RIGHT:
            if self.grid_pos + RIGHT not in self.app.walls:
                return True

        if self.stored_direction == UP:
            if self.grid_pos + UP not in self.app.walls:
                return True

        if self.stored_direction == DOWN:
            if self.grid_pos + DOWN not in self.app.walls:
                return True

        return False

    def move(self, direction):
        self.stored_direction = direction

    def rotate(self):
        if self.current_direction == RIGHT:
            self.image = pygame.transform.rotate(player_shrink_img, 0)
        elif self.current_direction == LEFT:
            self.image = pygame.transform.rotate(player_shrink_img, 180)
        elif self.current_direction == UP:
            self.image = pygame.transform.rotate(player_shrink_img, 90)
        elif self.current_direction == DOWN:
            self.image = pygame.transform.rotate(player_shrink_img, -90)
        else:
            self.image = pygame.transform.rotate(player_shrink_img, 0)

    def able_to_move(self):
        if Vector2(self.grid_pos + self.current_direction) in self.app.walls:
            return False
        else:
            return True  

    def eat_coin(self):
        if Vector2(self.grid_pos) in self.app.coins:
            chomp_sound.play(maxtime=50)
            self.app.coins.remove(Vector2(self.grid_pos))
            self.score += 1
            if self.score > self.app.high_score:
                self.app.high_score = self.score
                with open('high_score.txt', 'w') as file:
                    file.write(f"HIGHSCORE = {self.app.high_score}")

    def eat_pellet(self):
        if Vector2(self.grid_pos) in self.app.pellets:
            chomp_sound.play(maxtime=50)
            self.app.pellets.remove(Vector2(self.grid_pos))
            self.app.intermission = True
            print("start intermission")
            self.change_enemy_images()
            self.app.play_intermission_music()
            self.intermission_start_time = time.time()

    def change_enemy_images(self):
        for enemy in self.app.enemies:
            enemy.image = enemy_intermission_img

    def change_enemy_images_back(self):
        for enemy in self.app.enemies:
            if enemy.index == 0:
                enemy.image = blue_ghost_img
            if enemy.index == 1:
                enemy.image = pink_ghost_img
            if enemy.index == 2:
                enemy.image = orange_ghost_img
            if enemy.index == 3:
                enemy.image = red_ghost_img
            enemy.image = pygame.transform.scale(enemy.image, (18, 18))

    # player will keep on moving 
    # we will press the keys to only change direction 

    # switch on the intermission once the pellet is eaten, and keep it on for fixed seconds
    # if collision, we need increase the player points and reset
    # after time, we will intermission = False

    


    