import pygame
import time
import random
from cell import Cell
from maze import Maze

# set up pygame window
WIDTH = 1000
HEIGHT = 600
FPS = 500

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
w = 10                   # width of cell
maze_height = 400
maze_width = 600

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
    a = 0
    for i in range(w, maze_height + w, w):
        for j in range(w, maze_width + w, w):
            cell = Cell(j, i, w, maze_height=maze_height, maze_width=maze_width, id=a)
            maze.add_cell(cell)
            a += 1
    return maze


def build_grid(x=w, y=w, w=20):
    pygame.draw.rect(screen, YELLOW, (x, y, maze_width, maze_height), w // 2)
    pygame.draw.rect(screen, GRAY, (x - w // 4, y + w // 4, w // 2, w // 2))
    pygame.draw.rect(screen, GRAY, (maze_width + 3 * w // 4, maze_height + w // 4, w // 2, w // 2))


def blitter(which_one, algorithm):
    font = pygame.font.Font('freesansbold.ttf', 16)
    text = font.render(which_one, True, WHITE, RED, )
    text2 = font.render(algorithm, False, WHITE)
    textRect = text.get_rect()
    textRect2 = text2.get_rect()
    textRect.center = (maze_width + (WIDTH - maze_width) // 2, HEIGHT // 6)
    textRect2.center = (maze_width + (WIDTH - maze_width) // 2, HEIGHT // 6 + 50)
    screen.blit(text, textRect)
    screen.blit(text2, textRect2)


def unblitter():
    pygame.draw.rect(screen, (0, 0, 0), (maze_width + 25, 0, WIDTH - maze_width, HEIGHT))


def pathfinder(path):
    for i in reversed(range(len(path))):
        if i < len(path) - 1:
            path[i].make_path(path[i + 1], screen, color)
        color_ratio = 255 / len(path)
        color = int(i*color_ratio)
        color = (color, 0, 255 - color)
        path[i].update_cell(screen, color)
        clock.tick(FPS)
        pygame.display.update()



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
    current_cell.update_cell(screen, GRAY)
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
    pathfinder(path)
    print(len(path))
    print("-" * 82)


def bfs_solve_map():
    bfs_queue = []
    current_cell = maze.get_cell(0)
    current_cell.visited = True
    bfs_queue.append(current_cell)
    current_cell.update_cell(screen, GRAY)
    while current_cell.id < maze.cell_count() - 1:
        clock.tick(FPS)
        pygame.display.update()
        for event in pygame.event.get():
            # check for closing the window
            if event.type == pygame.QUIT:
                pygame.quit()
        current_cell = bfs_queue.pop(0)
        current_cell.update_cell(screen, GRAY)
        for edge in current_cell.edges:
            if edge.visited is False:
                edge.visited = True
                edge.parent = current_cell
                edge.make_path(current_cell, screen, GRAY)
                bfs_queue.append(edge)
    path = []
    while current_cell.id > 0:
        path.append(current_cell)
        current_cell = current_cell.parent
    path.append(current_cell)
    pathfinder(path)
    print(len(path))


def dijkstra():
    current_cell = maze.get_cell(0)
    current_cell.distance = 0
    unvisited_set = [item for item in maze.maze_dict.values()]
    while True:
        clock.tick(FPS)
        pygame.display.update()
        for event in pygame.event.get():
            # check for closing the window
            if event.type == pygame.QUIT:
                pygame.quit()
        for edge in current_cell.edges:
            temp_distance = current_cell.distance + 1
            edge.distance = min(edge.distance, temp_distance)
            if edge.visited is False:
                edge.parent = current_cell
        current_cell.visited = True
        current_cell.update_cell(screen, GRAY)
        unvisited_set.remove(current_cell)
        unvisited_set.sort(key=lambda k: k.distance)
        if maze.get_cell(maze.cell_count() - 1).visited or unvisited_set[0] is 2000000000:
            break
        else:
            current_cell = unvisited_set[0]
            current_cell.make_path(current_cell.parent, screen, GRAY)
    path = []
    while current_cell.id > 0:
        path.append(current_cell)
        current_cell = current_cell.parent
    path.append(current_cell)
    pathfinder(path)
    print(len(path))

state = "Initial"
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
        elif pygame.mouse.get_pressed()[0] and state is "Selection":
            pygame.draw.rect(screen, (0, 0, 0), (maze_width + 25, HEIGHT // 2, WIDTH - maze_width, HEIGHT // 2))
            font = pygame.font.Font('freesansbold.ttf', 16)
            text = font.render('Solve', True, WHITE, (0, 0, 128))
            text2 = font.render('Another Maze', False, WHITE)
            textRect = text.get_rect()
            textRect2 = text2.get_rect()
            textRect.center = (maze_width + (WIDTH - maze_width) // 2, 4 * HEIGHT // 6)
            textRect2.center = (maze_width + (WIDTH - maze_width) // 2, 4 * HEIGHT // 6 + 50)
            screen.blit(text, textRect)
            screen.blit(text2, textRect2)
            pos = pygame.mouse.get_pos()
            if textRect.collidepoint(pos):
                pygame.draw.rect(screen, (0, 0, 0), (maze_width + 25, HEIGHT // 2, WIDTH - maze_width, HEIGHT // 2))
                state = "Solve 1"
                font = pygame.font.Font('freesansbold.ttf', 16)
                text = font.render('Press Mouse to continue', True, WHITE, (0, 0, 128))
                textRect = text.get_rect()
                textRect.center = (maze_width + (WIDTH - maze_width) // 2, 4 * HEIGHT // 6)
                screen.blit(text, textRect)
            elif textRect2.collidepoint(pos):
                pygame.draw.rect(screen, (0, 0, 0), (maze_width + 25, HEIGHT // 2, WIDTH - maze_width, HEIGHT // 2))
                state = "Initial"
                font = pygame.font.Font('freesansbold.ttf', 16)
                text = font.render('Press Mouse to continue', True, WHITE, (0, 0, 128))
                textRect = text.get_rect()
                textRect.center = (maze_width + (WIDTH - maze_width) // 2, 4 * HEIGHT // 6)
                screen.blit(text, textRect)
        elif pygame.mouse.get_pressed()[0] and state is "Initial":
            pygame.draw.rect(screen, (0, 0, 0), (maze_width + 25, HEIGHT // 2, WIDTH - maze_width, HEIGHT // 2))
            screen.fill((0, 0, 0))
            maze = initialize_cells(w, w, w)
            build_grid(w, w, w)
            blitter("Maze Generating Algorithms", "Recursive Backtracking")
            generate_map()
            state = "Selection"
            font = pygame.font.Font('freesansbold.ttf', 16)
            text = font.render('Press Mouse to continue', True, WHITE, (0, 0, 128))
            textRect = text.get_rect()
            textRect.center = (maze_width + (WIDTH - maze_width) // 2, 4 * HEIGHT // 6)
            screen.blit(text, textRect)
        elif pygame.mouse.get_pressed()[0] and state is "Solve 1":
            pygame.draw.rect(screen, (0, 0, 0), (maze_width + 25, HEIGHT // 2, WIDTH - maze_width, HEIGHT // 2))
            maze.make_unvisited()
            unblitter()
            blitter("Maze Solving Algorithms", "Depth First Search")
            dfs_solve_map()
            state = "Solve 2"
            font = pygame.font.Font('freesansbold.ttf', 16)
            text = font.render('Press Mouse to continue', True, WHITE, (0, 0, 128))
            textRect = text.get_rect()
            textRect.center = (maze_width + (WIDTH - maze_width) // 2, 4 * HEIGHT // 6)
            screen.blit(text, textRect)
        elif pygame.mouse.get_pressed()[0] and state is "Solve 2":
            pygame.draw.rect(screen, (0, 0, 0), (maze_width + 25, HEIGHT // 2, WIDTH - maze_width, HEIGHT // 2))
            maze.clear_paths(screen)
            maze.make_unvisited()
            unblitter()
            blitter("Maze Solving Algorithms", "Breadth First Search")
            bfs_solve_map()
            state = "Solve 3"
            font = pygame.font.Font('freesansbold.ttf', 16)
            text = font.render('Press Mouse to continue', True, WHITE, (0, 0, 128))
            textRect = text.get_rect()
            textRect.center = (maze_width + (WIDTH - maze_width) // 2, 4 * HEIGHT // 6)
            screen.blit(text, textRect)
        elif pygame.mouse.get_pressed()[0] and state is "Solve 3":
            pygame.draw.rect(screen, (0, 0, 0), (maze_width + 25, HEIGHT // 2, WIDTH - maze_width, HEIGHT // 2))
            maze.clear_paths(screen)
            maze.make_unvisited()
            unblitter()
            blitter("Maze Solving Algorithms", "Dijkstra")
            dijkstra()
            state = "Initial"
            font = pygame.font.Font('freesansbold.ttf', 16)
            text = font.render('Press Mouse to continue', True, WHITE, (0, 0, 128))
            textRect = text.get_rect()
            textRect.center = (maze_width + (WIDTH - maze_width) // 2, 4 * HEIGHT // 6)
            screen.blit(text, textRect)


