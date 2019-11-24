import pygame
from cell import Cell


class Maze:
    def __init__(self):
        self.maze_dict = {}

    def add_cell(self, cell):
        self.maze_dict[cell.id] = cell
        print(self.maze_dict)

    def cell_count(self):
        return len(self.maze_dict)

    def get_cell(self, idx):
        return self.maze_dict[idx]

    # def draw_screen(self, screen):
    #     for item in self.maze_dict.values():
    #         Cell.update_cell(item, screen)