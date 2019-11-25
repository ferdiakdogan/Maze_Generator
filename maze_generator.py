import pygame
import time
import random
from cell import Cell
from maze import Maze

# set up pygame window
WIDTH = 480
HEIGHT = 600
FPS = 1000

# Define colours
WHITE = (255, 255, 255)
GREEN = (0, 255, 0,)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (125, 125, 125)
YELLOW = (200, 200, 0)


# setup maze variables
x = 0                    # x axis
y = 0                    # y axis
w = 4                   # width of cell
maze_height = 400
maze_width = 400

# Stack
cell_stack = []

# initalize Pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Maze Generator")
clock = pygame.time.Clock()


# setup the grid
def initialize_cells(x=w, y=w, w=20):
    maze = Maze(maze_width, maze_height, w)
    for y in range(w, maze_height + w, w):
        for x in range(w, maze_width + w, w):
            cell = Cell(x, y, w, maze_height=maze_height, maze_width=maze_width)
            maze.add_cell(cell)
    return maze


def build_grid(x=w, y=w, w=20):
    pygame.draw.rect(screen, YELLOW, (x, y, maze_width, maze_height), w // 2)
    pygame.draw.rect(screen, GRAY, (x - w // 4, y + w // 4, w // 2, w // 2))
    pygame.draw.rect(screen, GRAY, (maze_width + 3 * w // 4, maze_height + w // 4, w // 2, w // 2))


def generate_map():
    visited_count = 0
    cell_count = maze.cell_count()
    initial_cell = random.randint(0, cell_count - 1)
    current_cell = maze.get_cell(initial_cell)
    current_cell.visited = True
    visited_count += 1
    current_cell.update_cell(screen)
    maze.cell_neighbors()
    while visited_count < cell_count:
        clock.tick(FPS)
        pygame.display.update()
        for event in pygame.event.get():
            # check for closing the window
            if event.type == pygame.QUIT:
                pygame.quit()
        if current_cell.check_neighbors():
            chosen_neighbor = current_cell.choose_neighbor()
            cell_stack.append(current_cell)
            current_cell.remove_wall(chosen_neighbor, screen)
            current_cell.update_cell(screen, WHITE)
            current_cell = chosen_neighbor
            current_cell.visited = True
            visited_count += 1
            current_cell.update_cell(screen, BLUE)
        elif cell_stack:
            current_cell.update_cell(screen, WHITE)
            current_cell = cell_stack.pop()
            current_cell.update_cell(screen, BLUE)
    current_cell.update_cell(screen, WHITE)
    print("-"*82)


def dfs_solve_map():
    dfs_stack = []
    path = []
    current_cell = maze.get_cell(0)
    current_cell.visited = True
    path.append(current_cell)
    current_cell.update_cell(screen, BLUE)
    while current_cell.id < maze.cell_count() - 1:
        clock.tick(FPS)
        pygame.display.update()
        for event in pygame.event.get():
            # check for closing the window
            if event.type == pygame.QUIT:
                pygame.quit()
        if current_cell.check_edges():
            chosen_edge = current_cell.choose_edge()
            dfs_stack.append(current_cell)
            current_cell.make_path(chosen_edge, screen, GRAY)
            current_cell.update_cell(screen, GRAY)
            current_cell = chosen_edge
            path.append(current_cell)
            current_cell.visited = True
            current_cell.update_cell(screen, GRAY)
        elif dfs_stack:
            current_cell.update_cell(screen, WHITE)
            popped = dfs_stack.pop()
            popped.update_cell(screen, GRAY)
            current_cell.make_path(popped, screen, WHITE)
            path.pop()
            current_cell = popped
    current_cell.update_cell(screen, GRAY)
    for i in reversed(range(len(path))):
        if i < len(path) - 1:
            path[i].make_path(path[i + 1], screen, color)
        color_ratio = 255 / len(path)
        color = int(i*color_ratio)
        color = (color, 0, 255 - color)
        path[i].update_cell(screen, color)
        clock.tick(FPS)
        pygame.display.update()

    print("-" * 82)


maze = initialize_cells(w, w, w)
build_grid(w, w, w)
generate_map()
maze.make_unvisited()
dfs_solve_map()

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

