import sys
import pygame
from settings import *

pygame.init()

class App:

    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'start'
        
    def run(self):
        while self.running == True:
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

################################# START SCREEN #######################################

    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def start_redraw(self):
        self.screen.fill(BLACK)
        self.draw_text("HIGH SCORE - 0", self.screen, DEFAULT_FONT, DEFAULT_SIZE, WHITE, [5, 0])
        self.draw_text("PUSH SPACE BAR", self.screen, DEFAULT_FONT, DEFAULT_SIZE, ORANGE, [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 50], centered=True)
        self.draw_text("1 PLAYER ONLY", self.screen, DEFAULT_FONT, DEFAULT_SIZE, BLUE, [SCREEN_WIDTH // 2, 2 * SCREEN_HEIGHT // 3 - 50], centered=True)
        pygame.display.update()

################################# PLAY SCREEN #######################################

    def play_events(self):
        pass

    def play_redraw(self):
        pass


    


