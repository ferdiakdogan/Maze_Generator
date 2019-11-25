import pygame
import random

WHITE = (255, 255, 255)
GREEN = (0, 255, 0,)
BLUE = (0, 0, 255)
RED = (255, 0, 0)


class Cell:
    def __init__(self, x, y, screen, width=20, left=True, right=True,
                 top=True, bottom=True, visited=False, maze_height=200, maze_width=200):
        self.x = x
        self.y = y
        self.width = width
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        self.visited = visited
        self.maze_height = maze_height
        self.maze_width = maze_width
        self.id = self.maze_height // self.width * (self.y - self.width) // self.width + (self.x - self.width) // self.width
        self.left_cell = None
        self.right_cell = None
        self.top_cell = None
        self.bottom_cell = None
        self.neighbors = []

    def update_cell(self, screen, color=WHITE):
        if self.visited:
            pygame.draw.rect(screen, color, (self.x + self.width // 4, self.y + self.width // 4, self.width // 2, self.width // 2))

    def check_neighbors(self):
        for item in self.neighbors:
            if item is not None:
                if item.visited is False:
                    return True

    def choose_neighbor(self):
        available_neighbors = [item for item in self.neighbors if item.visited is False]
        chosen_neighbor = random.choice(available_neighbors)
        return chosen_neighbor

    def remove_wall(self, other, screen):
        pygame.draw.rect(screen, WHITE, ((self.x + other.x) // 2 + self.width // 4, (self.y + other.y) // 2 + self.width // 4, self.width // 2, self.width // 2))


