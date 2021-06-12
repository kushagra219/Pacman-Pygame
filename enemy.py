import pygame
pygame.mixer.init()
from settings import *
from pygame.math import Vector2
import random
import copy

blue_ghost_img = pygame.image.load('assets/pacman-blue-ghost.jpg')
pink_ghost_img = pygame.image.load('assets/pacman-pink-ghost.jpg')
orange_ghost_img = pygame.image.load('assets/pacman-orange-ghost.jpg')
red_ghost_img = pygame.image.load('assets/pacman-red-ghost.jpg')

collision_sound = pygame.mixer.Sound('assets/pacman_death.wav')

class Enemy(object):
    def __init__(self, app, pos, idx):
        self.app = app
        self.index = idx
        self.image = self.select_image()
        self.image = pygame.transform.scale(self.image, (18, 18))
        self.personality = self.select_personality()
        self.starting_pos = pos
        self.grid_pos = pos
        self.pix_pos = self.get_pix_pos()
        self.color = self.select_color()
        self.direction = Vector2(0, 0)
        self.first_run = True
        self.speed = self.select_speed()

    def get_pix_pos(self):
        x = TOP_BOTTOM_SPACE // 2 + self.grid_pos.x * self.app.cell_width 
        y =  TOP_BOTTOM_SPACE // 2 + self.grid_pos.y * self.app.cell_height
        return Vector2(x, y)

    def get_grid_pos(self):
        x = (self.pix_pos.x - TOP_BOTTOM_SPACE // 2)  \
            // self.app.cell_width
        y = (self.pix_pos.y - TOP_BOTTOM_SPACE // 2)  \
            // self.app.cell_height
        return Vector2(x, y)

    def draw(self):
        self.app.screen.blit(self.image, 
        (TOP_BOTTOM_SPACE // 2 + self.grid_pos.x * self.app.cell_width, 
        TOP_BOTTOM_SPACE // 2 + self.grid_pos.y * self.app.cell_height))
        # pygame.draw.circle(self.app.screen, self.color, self.pix_pos, self.app.cell_width // 2 - 2, 0)
        self.move()

    def move(self):
        if self.personality == 'random':
            self.direction = self.get_random_direction()
        
        elif self.personality == 'scared':
            if self.first_run == True:
                self.grid_pos = Vector2(13, 23)
                self.pix_pos = self.get_pix_pos()
                self.first_run = False
            self.direction = self.get_scared_direction()

        else:
            if self.app.intermission == False:
                next_cell = self.get_next_cell()
                self.direction = next_cell - self.grid_pos
            else:
                self.direction = self.get_scared_direction()

        if self.able_to_move() == True:
            self.pix_pos += self.direction * self.speed
            self.grid_pos = self.get_grid_pos()
        
        self.check_collision()
            

    def check_collision(self):
        if self.grid_pos == self.app.player.grid_pos:
            # collision_sound.play()
            if self.app.intermission == False:
                self.app.player.lives -= 1
                
                print("Lives left: ", self.app.player.lives)
                if self.app.player.lives == 0:
                    self.app.state = 'game-over'
                    self.app.play_start_music()
                    return

                self.app.player.grid_pos = Vector2(13, 29)
                self.app.player.pix_pos = self.app.player.get_pix_pos()
                self.app.player.current_direction = Vector2(0, 0)
                self.app.reset_enemies()
                self.app.player.draw()
                pygame.display.update()
                pygame.time.delay(250)
            else:
                self.app.player.score += 100
                self.app.draw_text("100", self.app.screen, DEFAULT_FONT, 10, WHITE, self.pix_pos - Vector2(10, 10))
                self.grid_pos = copy.deepcopy(self.app.enemies_pos[self.index])
                self.pix_pos = self.get_pix_pos()
                pygame.display.update()
                pygame.time.delay(500)


    def get_random_direction(self):
        return random.choice([UP, DOWN, LEFT, RIGHT])

    def get_scared_direction(self):
        path = self.get_bfs_path()
        neighbours = [UP, DOWN, LEFT, RIGHT]
        for i in neighbours:
            curr_neighbour = self.grid_pos + i
            if self.isSafe(curr_neighbour) and \
                curr_neighbour not in path:
                return curr_neighbour - self.grid_pos
        return (path[1] - self.grid_pos) if len(path) > 1 \
        else (path[0] - self.grid_pos)
    
    def get_next_cell(self):
        path = self.get_bfs_path()
        return Vector2(path[1]) if len(path) > 1 else Vector2(path[0])

    def get_bfs_path(self):  
        # source is the enemy position
        src = self.grid_pos
        # target is the player position
        target = self.app.player.grid_pos
        # parent (parent of key is value)
        parent = {}
        # append the source into the queue
        queue = [src]
        # parent of source is [-1, -1]
        parent[tuple(src)] = Vector2(-1, -1)
        # neighbours are top, down, left, right
        neighbours = [UP, DOWN, LEFT, RIGHT]

        # run this loop till queue becomes empty
        while len(queue) > 0:
            # first element is the current cell
            curr_cell = queue[0]
            # remove the current cell from the queue
            queue.remove(queue[0])
            # curr_cell becomes the target, then we have reached the 
            # destination, so break
            if curr_cell == target:
                break
            # otherwise, go to every neighbour of current cell 
            for i in neighbours:
                neighbour_cell = curr_cell + i
                # if the nighbour is not a wall, is valid and is not visited
                if self.isSafe(neighbour_cell) == True and \
                tuple(neighbour_cell) not in parent:
                    # append the neighbour into the queue
                    queue.append(neighbour_cell)
                    # parent of neighbour cell would be current cell
                    parent[tuple(neighbour_cell)] = curr_cell
        
        # path initilaization
        path = [target]
        # starting from target, travel back to the source using parent
        while parent[tuple(target)] != Vector2(-1, -1):
            # append the parent of the target
            path.append(parent[tuple(target)])
            # reassign the target to parent of target (travelling back)
            target = parent[tuple(target)]
    
        # reverse the path and return
        path.reverse()
        return path

    def isSafe(self, cell):
        # check for boundaries and check if cell is not a wall
        return (cell.x >= 0) and (cell.y >= 0) and (cell.x <= 27) and \
        (cell.y <= 30) and (cell not in self.app.walls)

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

    def select_image(self):
        if self.index == 0:
            return blue_ghost_img
        if self.index == 1:
            return pink_ghost_img
        if self.index == 2:
            return orange_ghost_img
        if self.index == 3:
            return red_ghost_img

    def select_personality(self):
        if self.index == 0:
            return "slow"
        if self.index == 1:
            return "random"
        if self.index == 2:
            return "scared"
        if self.index == 3:
            return "speedy"

    def select_speed(self):
        if self.index == 0:
            return 5
        if self.index == 1:
            return 10
        if self.index == 2:
            return 10
        if self.index == 3:
            return 20

