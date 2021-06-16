import sys
import copy
import pygame
from settings import *
from player import Player
from enemy import Enemy
from pygame.math import Vector2
import sqlite3

pygame.init()

class App:

    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pacman")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'start'
        self.cell_width = 20
        self.cell_height = 20
        self.player = Player(self, Vector2(13, 29))
        self.cells = []
        self.walls = []
        self.coins = []
        self.pellets = []
        self.enemies = []
        self.enemies_pos = []
        self.high_score = self.get_high_score()
        self.load()
        self.make_enemies()
        self.play_start_music()
        self.intermission = False
        self.pellet_blink_counter = 0
        
    def run(self):
        while self.running == True:
            self.clock.tick(FPS)
            if self.state == 'start':
                self.start_events()
                self.start_redraw()
            elif self.state == 'play':
                self.play_events()
                self.play_redraw()
            elif self.state == 'game-over':
                self.game_over_events()
                self.game_over_redraw()
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
        self.background = pygame.image.load(resource_path('assets/maze.png'))
        with open(resource_path("walls.txt")) as file:
            lines = file.readlines()
            for line in lines:
                self.cells.append(line[:-1])

        for row in range(ROWS):
            for col in range(COLS):
                if self.cells[row][col] == '1':
                    self.walls.append(Vector2(col, row))
                elif self.cells[row][col] == 'C':
                    self.coins.append(Vector2(col, row))
                elif self.cells[row][col] in ['2', '3', '4', '5']:
                    self.enemies_pos.append(Vector2(col, row))
                elif self.cells[row][col] == 'B':
                    pygame.draw.rect(self.background, BLACK, (col * self.cell_width, row * self.cell_height, self.cell_width, self.cell_height), 0)
                elif self.cells[row][col] == 'I':
                    self.pellets.append(Vector2(col, row))
    
    def make_enemies(self):
        for idx, pos in enumerate(self.enemies_pos):
            new_enemy = Enemy(self, copy.deepcopy(pos), idx)
            self.enemies.append(new_enemy)

    def draw_grid(self):
        for x in range(SCREEN_WIDTH // self.cell_width):
            pygame.draw.line(self.background, GRAY_LIGHT, (x * self.cell_width, 0), (x * self.cell_width, MAZE_HEIGHT), 1)
        
        for y in range(SCREEN_HEIGHT // self.cell_height):
            pygame.draw.line(self.background, GRAY_LIGHT, (0, y * self.cell_height), (MAZE_WIDTH, y * self.cell_height), 1)
        
        for wall in self.walls:
            pygame.draw.rect(self.background, BLUE, (wall.x * self.cell_width, wall.y * self.cell_height, self.cell_width, self.cell_height), 0)
         
    def draw_coins(self):
        for coin in self.coins:
            pygame.draw.circle(self.screen, WHITE, (TOP_BOTTOM_SPACE // 2 + coin.x * self.cell_width + self.cell_width // 2, TOP_BOTTOM_SPACE // 2 + coin.y * self.cell_height + self.cell_height // 2), self.cell_width // 2 - 8, 0)

    def draw_pellets(self):
        self.pellet_blink_counter += 1
        if self.pellet_blink_counter % 2 == 0:
            for pellet in self.pellets:
                pygame.draw.circle(self.screen, WHITE, (TOP_BOTTOM_SPACE // 2 + pellet.x * self.cell_width + self.cell_width // 2, TOP_BOTTOM_SPACE // 2 + pellet.y * self.cell_height + self.cell_height // 2), self.cell_width // 2 - 2, 0)
    
    def get_high_score(self):
        with open(resource_path('high_score.txt'), 'rt') as file:
            high_score = int(file.readline().split(" ")[2])
        return high_score

    def reset_enemies(self):
        self.enemies = []
        self.make_enemies()

    def reset(self):
        self.player.score = 0
        self.player.lives = 3
        self.player.grid_pos = Vector2(13, 29)
        self.player.pix_pos = self.player.get_pix_pos()
        self.player.current_direction = Vector2(0, 0)
        self.player.stored_direction = Vector2(0, 0)

        self.reset_enemies()

        self.coins = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.cells[row][col] == 'C':
                    self.coins.append(Vector2(col, row))
        
        self.play_play_music()

    def play_start_music(self):
        pygame.mixer.music.load(resource_path('assets/pacman_beginning.wav'))
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.3)

    def play_play_music(self):
        pygame.mixer.music.load(resource_path('assets/Pac_Man_Ghost_Noises.mp3'))
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.3)

    def play_intermission_music(self):
        pygame.mixer.music.load(resource_path('assets/pacman_intermission.wav'))
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.3)

################################# START SCREEN #######################################

    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.state = 'play'
                    self.play_play_music()

    def start_redraw(self):
        self.screen.fill(BLACK)
        self.draw_text(f"HIGH SCORE - {self.high_score}", self.screen, DEFAULT_FONT, DEFAULT_SIZE, WHITE, [5, 0])
        self.draw_text("PUSH SPACE BAR", self.screen, DEFAULT_FONT, DEFAULT_SIZE, ORANGE, [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 50], centered=True)
        self.draw_text("1 PLAYER ONLY", self.screen, DEFAULT_FONT, DEFAULT_SIZE, BLUE, [SCREEN_WIDTH // 2, 2 * SCREEN_HEIGHT // 3 - 50], centered=True)
        pygame.display.update()


################################# PLAY SCREEN #######################################

    def play_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.player.move(Vector2(0, -1))
                if event.key == pygame.K_DOWN:
                    self.player.move(Vector2(0, 1))
                if event.key == pygame.K_LEFT:
                    self.player.move(Vector2(-1, 0))
                if event.key == pygame.K_RIGHT:
                    self.player.move(Vector2(1, 0))

        # keys_pressed = pygame.key.get_pressed()
        # if keys_pressed[pygame.K_UP] == True:
        #     self.player.move(Vector2(0, -1))
        # if keys_pressed[pygame.K_DOWN] == True:
        #     self.player.move(Vector2(0, 1))
        # if keys_pressed[pygame.K_LEFT] == True:
        #     self.player.move(Vector2(-1, 0))
        # if keys_pressed[pygame.K_RIGHT] == True:
        #     self.player.move(Vector2(1, 0))

    def play_redraw(self):
        self.screen.fill(BLACK)
        self.draw_text(f"CURRENT SCORE - {self.player.score}", self.screen, DEFAULT_FONT, DEFAULT_SIZE, WHITE, [60, 0])
        self.draw_text(f"HIGH SCORE - {self.high_score}", self.screen, DEFAULT_FONT, DEFAULT_SIZE, WHITE, [SCREEN_WIDTH//2 + 50, 0])
        self.screen.blit(self.background, (TOP_BOTTOM_SPACE // 2, TOP_BOTTOM_SPACE//2))
        self.draw_coins()
        self.draw_pellets()
        # self.draw_grid()
        self.player.draw()
        for enemy in self.enemies:
            enemy.draw()
        pygame.display.update()


################################# GAME OVER SCREEN #######################################

    # GAME OVER
    # Press SPACE bar to PLAY AGAIN
    # Press the escape button to QUIT

    def game_over_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_SPACE:
                    self.reset()
                    self.state = 'play'

    def game_over_redraw(self):
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", self.screen, DEFAULT_FONT, 50, 
        RED, [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4], centered=True)
        self.draw_text("Press SPACE bar to PLAY AGAIN", self.screen, DEFAULT_FONT, 25, 
        GRAY_LIGHT, [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2], centered=True)
        self.draw_text("Press the escape button to QUIT", self.screen, DEFAULT_FONT, 25, 
        GRAY_LIGHT, [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50], centered=True)
        pygame.display.update()

    

    


