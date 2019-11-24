import pygame

WHITE = (255, 255, 255)
GREEN = (0, 255, 0,)
BLUE = (0, 0, 255)
RED = (255, 0, 0)


class Cell:
    def __init__(self, x, y, screen, width=20, left=True, right=True,
                 top=True, bottom=True, visited=False, maze_height=200, maze_widht=200):
        self.x = x
        self.y = y
        self.width = width
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        self.visited = visited
        self.maze_height = maze_height
        self.maze_width = maze_widht
        self.id = self.maze_height // self.width * (self.y - self.width) // self.width + (self.x - self.width) // self.width
        if self.x is self.width:
            self.left_cell = None
        else:
            self.left_cell = False
        if self.x is self.maze_width + self.width:
            self.right_cell = None
        else:
            self.right_cell = False
        if self.y is self.width:
            self.top_cell = None
        else:
            self.top_cell = False
        if self.y is self.width + self.maze_height:
            self.bottom_cell = None
        else:
            self.bottom_cell = False

    def update_cell(self, screen):
        if self.right:
            pygame.draw.line(screen, WHITE, [self.x + self.width, self.y], [self.x + self.width, self.y + self.width], 6)
        if self.left:
            pygame.draw.line(screen, WHITE, [self.x, self.y], [self.x, self.y + self.width], 6)
        if self.top:
            pygame.draw.line(screen, WHITE, [self.x, self.y], [self.x + self.width, self.y], 6)
        if self.bottom:
            pygame.draw.line(screen, WHITE, [self.x, self.y + self.width], [self.x + self.width, self.y + self.width], 6)
        if self.visited:
            pygame.draw.rect(screen, BLUE, (self.x + 3, self.y + 3, self.width - 3, self.width - 3))

    def compare_neighbors(self):
        if self.left_cell or self.right_cell or self.bottom_cell or self.top_cell is False:
            return True
