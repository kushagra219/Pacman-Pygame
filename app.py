import sys
import pygame
from settings import *
from player import Player
from pygame.math import Vector2

pygame.init()

class App:

    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'start'
        self.cell_width = 20
        self.cell_height = 20
        self.player = Player(self, Vector2(1, 1))
        self.walls = []
        self.load()
        
    def run(self):
        while self.running == True:
            self.clock.tick(FPS)
            if self.state == 'start':
                self.start_events()
                self.start_redraw()
            elif self.state == 'play':
                self.play_events()
                self.play_redraw()
        pygame.quit()
        sys.exit()

################################# HELPER FUNCTIONS ###################################

    def draw_text(self, text, screen, font_type, font_size, font_color, pos, centered=False):
        font = pygame.font.SysFont(font_type, font_size)
        text = font.render(text, False, font_color)
        if centered == True:
            pos[0] = pos[0] - text.get_size()[0] // 2
            pos[1] = pos[1] - text.get_size()[1] // 2
        screen.blit(text, pos)

    def load(self):
        self.background = pygame.image.load('assets/maze.png')
        with open("walls.txt") as file:
            lines = file.readlines()
            for line in lines:
                self.walls.append(line[:-1])


    def draw_grid(self):
        for x in range(SCREEN_WIDTH // self.cell_width):
            pygame.draw.line(self.background, GRAY_LIGHT, (x * self.cell_width, 0), (x * self.cell_width, MAZE_HEIGHT), 1)
        
        for y in range(SCREEN_HEIGHT // self.cell_height):
            pygame.draw.line(self.background, GRAY_LIGHT, (0, y * self.cell_height), (MAZE_WIDTH, y * self.cell_height), 1)

        for row in range(len(self.walls)):
            for col in range(row):
                try:
                    if self.walls[row][col] == '1':
                        pygame.draw.rect(self.background, GREEN, (row * self.cell_width, col * self.cell_height, self.cell_width, self.cell_height), 0)
                except:
                    print(self.walls[row])

################################# START SCREEN #######################################

    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.state = 'play'

    def start_redraw(self):
        self.screen.fill(BLACK)
        self.draw_text("HIGH SCORE - 0", self.screen, DEFAULT_FONT, DEFAULT_SIZE, WHITE, [5, 0])
        self.draw_text("PUSH SPACE BAR", self.screen, DEFAULT_FONT, DEFAULT_SIZE, ORANGE, [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 50], centered=True)
        self.draw_text("1 PLAYER ONLY", self.screen, DEFAULT_FONT, DEFAULT_SIZE, BLUE, [SCREEN_WIDTH // 2, 2 * SCREEN_HEIGHT // 3 - 50], centered=True)
        pygame.display.update()

################################# PLAY SCREEN #######################################

    def play_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_UP] == True:
            self.player.move(Vector2(0, -1))
        if keys_pressed[pygame.K_DOWN] == True:
            self.player.move(Vector2(0, 1))
        if keys_pressed[pygame.K_LEFT] == True:
            self.player.move(Vector2(-1, 0))
        if keys_pressed[pygame.K_RIGHT] == True:
            self.player.move(Vector2(1, 0))

    def play_redraw(self):
        self.screen.fill(BLACK)
        self.draw_text("CURRENT SCORE - 0", self.screen, DEFAULT_FONT, DEFAULT_SIZE, WHITE, [60, 0])
        self.draw_text("HIGH SCORE - 0", self.screen, DEFAULT_FONT, DEFAULT_SIZE, WHITE, [SCREEN_WIDTH//2 + 50, 0])
        self.screen.blit(self.background, (TOP_BOTTOM_SPACE//2, TOP_BOTTOM_SPACE//2))
        self.draw_grid()
        self.player.draw()
        pygame.display.update()

    


