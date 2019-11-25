import pygame
from cell import Cell


class Maze:
    def __init__(self, maze_width=200, maze_height=200, w=20):
        self.maze_dict = {}
        self.maze_width = maze_width
        self.maze_height = maze_height
        self.w = w

    def add_cell(self, cell):
        self.maze_dict[cell.id] = cell

    def cell_count(self):
        return len(self.maze_dict)

    def get_cell(self, idx):
        return self.maze_dict[idx]

    def cell_neighbors(self):
        for idx in range(len(self.maze_dict)):
            if self.maze_dict[idx].x > self.w:
                self.maze_dict[idx].left_cell = self.maze_dict[idx - 1]
                self.maze_dict[idx].neighbors.append(self.maze_dict[idx].left_cell)
            else:
                self.maze_dict[idx].left_cell = None
            if self.maze_dict[idx].x < self.maze_width:
                self.maze_dict[idx].right_cell = self.maze_dict[idx + 1]
                self.maze_dict[idx].neighbors.append(self.maze_dict[idx].right_cell)
            else:
                self.maze_dict[idx].right_cell = None
            if idx >= self.maze_height // self.w:
                self.maze_dict[idx].top_cell = self.maze_dict[idx - self.maze_height // self.w]
                self.maze_dict[idx].neighbors.append(self.maze_dict[idx].top_cell)
            else:
                self.maze_dict[idx].top_cell = None
            if idx < len(self.maze_dict) - self.maze_height // self.w:
                self.maze_dict[idx].bottom_cell = self.maze_dict[idx + self.maze_height // self.w]
                self.maze_dict[idx].neighbors.append(self.maze_dict[idx].bottom_cell)
            else:
                self.maze_dict[idx].bottom_cell = None
        return
