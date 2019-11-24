import pygame
import time
import random
from cell import Cell
from maze import Maze

# set up pygame window
WIDTH = 480
HEIGHT = 600
FPS = 30

# Define colours
WHITE = (255, 255, 255)
GREEN = (0, 255, 0,)
BLUE = (0, 0, 255)
RED = (255, 0, 0)


# setup maze variables
x = 0                    # x axis
y = 0                    # y axis
w = 20                   # width of cell
maze_height = 200
maze_width = 200


# initalize Pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Maze Generator")
clock = pygame.time.Clock()


# setup the grid
def initialize_cells(x=w, y=w, w=20):
    maze = Maze()
    for y in range(w, maze_height + w, w):
        for x in range(w, maze_width + w, w):
            cell = Cell(x, y, screen, w)
            maze.add_cell(cell)
    return maze


def build_grid(x=w, y=w, w=20):
    for x in range(w, maze_width + 2*w, w):
        pygame.draw.line(screen, WHITE, [x, y], [x, y + maze_height], 6)
    x = w
    for y in range(w, maze_height + 2*w, w):
        pygame.draw.line(screen, WHITE, [x, y], [x + maze_width, y], 6)


def generate_map():
    cell_count = maze.cell_count()
    initial_cell = random.randint(0, cell_count)
    current_cell = maze.get_cell(initial_cell)
    current_cell.visited = True
    current_cell.update_cell(screen)
    while current_cell.compare_neighbors():
        pass


maze = initialize_cells(w, w, w)
build_grid(w, w, w)
generate_map()


running = True
while running:
    # keep running at the at the right speed
    clock.tick(FPS)
    pygame.display.update()
    # process input (events)
    for event in pygame.event.get():
        # check for closing the window
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

