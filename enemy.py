import pygame
from settings import *
from pygame.math import Vector2
import random

class Enemy(object):
    def __init__(self, app, pos, idx):
        self.app = app
        self.starting_pos = pos
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
        if self.index == 0:
            self.direction = self.get_random_direction()
        
        # elif self.index == 1:
        else:
            next_cell = self.get_next_cell()
            self.direction = next_cell - self.grid_pos

        if self.able_to_move() == True:
            self.grid_pos += self.direction
            self.pix_pos = self.get_pix_pos()
        
        if self.grid_pos == self.app.player.grid_pos:
            self.app.player.lives -= 1
            
            print("Lives left: ", self.app.player.lives)
            if self.app.player.lives == 0:
                self.app.state = 'game-over'
                return

            self.app.player.grid_pos = Vector2(13, 29)
            self.app.player.direction = Vector2(0, 0)
            self.app.player.draw()
            pygame.display.update()
            pygame.time.delay(100)
                
        for _ in range(10000):
            pass

    def get_random_direction(self):
        return random.choice([UP, DOWN, LEFT, RIGHT])

    
    def get_next_cell(self):
        path = self.get_bfs_path()
        return Vector2(path[1])

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
            # curr_cell becomes the target, then we have reached the destination, so break
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
        
        # pth initilaization
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

