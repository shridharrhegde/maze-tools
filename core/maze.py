"""
MAZE CLASS
"""

import pygame
import random


class Cell:
    def __init__(self, x, y):
        # walls
        self.left = True
        self.right = True
        self.top = True
        self.bottom = True

        # coordinates
        self.x = x
        self.y = y

        # graph params
        self.visited = False


class Maze:
    def __init__(self, width=0, cell_size=20, wall_t=1):
        # main params
        self.width = width
        self.cell_size = cell_size
        self.wall_t = wall_t

        # assert width sanity
        if not 0 <= width < 256:
            raise ValueError("")

        # initialize cells
        self.cells = [Cell(x, y) for y in range(width) for x in range(width)]

    def __unvisited_neighbors(self, cell):
        # return list of free neighbots
        neighbors = []

        index = self.get_index(cell.x, cell.y)
        end = self.width - 1

        # get all neighboring cells
        cell_l = self.cells[self.__limit(index - 1)]
        cell_r = self.cells[self.__limit(index + 1)]
        cell_t = self.cells[self.__limit(index - self.width)]
        cell_b = self.cells[self.__limit(index + self.width)]

        # check if the cells exist and are free
        if cell.x != 0 and not cell_l.visited:
            neighbors.append(cell_l)
        if cell.y != 0 and not cell_t.visited:
            neighbors.append(cell_t)
        if cell.x != end and not cell_r.visited:
            neighbors.append(cell_r)
        if cell.y != end and not cell_b.visited:
            neighbors.append(cell_b)

        return neighbors

    def __limit(self, num):
        # force limit to avoid IndexError
        return max(min(num, self.width ** 2 - 1), 0)

    def __set_wall(self, cell_1, cell_2, wall_set):
        # set wall boolean between cell_1 and cell_2

        # check adjacency
        if not self.is_adjacent(cell_1, cell_2):
            print("\033[33mWarning :\033[0m", end=" ")
            print("cannot set non-adjacent cells")
            return

        # difference
        x_diff = cell_1.x - cell_2.x
        y_diff = cell_1.y - cell_2.y

        if x_diff == 1:
            # cell_2 <-> cell_1
            cell_1.left = wall_set
            cell_2.right = wall_set
        elif x_diff == -1:
            # cell_1 <-> cell_2
            cell_1.right = wall_set
            cell_2.left = wall_set
        elif y_diff == 1:
            # cell_2 on top
            cell_1.top = wall_set
            cell_2.bottom = wall_set
        elif y_diff == -1:
            # cell_1 on top
            cell_1.bottom = wall_set
            cell_2.top = wall_set

    def create_wall(self, cell_1, cell_2):
        # create wall between cell_1 and cell_2
        self.__set_wall(cell_1, cell_2, wall_set=True)

    def remove_wall(self, cell_1, cell_2):
        # remove wall between cell_1 and cell_2
        self.__set_wall(cell_1, cell_2, wall_set=False)

    def is_adjacent(self, cell_1, cell_2):
        # check adjacency of two cells
        
        # difference
        x_diff = cell_1.x - cell_2.x
        y_diff = cell_1.y - cell_2.y

        # check adjacency
        cond_1 = abs(x_diff) == 1 and y_diff == 0
        cond_2 = abs(y_diff) == 1 and x_diff == 0
        cond_3 = x_diff == 0 and y_diff == 0

        # get return value
        retval = True if cond_1 or cond_2 or cond_3 else False
        return retval

    def get_index(self, x, y):
        # get 1d index from 2d coordinates
        return x + y * self.width

    def get_cell(self, x, y):
        # get cell at (x, y)
        return self.cells[x + y * self.width]

    def generate(self):
        # set 0, 0 as initial position
        curr_cell = self.cells[0]
        curr_cell.visited = True

        stack = [curr_cell]

        while stack:
            # get current cell
            curr_cell = stack.pop()

            # get unvisited neighbors list
            neigh = self.__unvisited_neighbors(curr_cell)

            if neigh:
                stack.append(curr_cell)

                # choose random direction
                next_cell = random.choice(neigh)
                next_cell.visited = True

                # remove wall
                self.remove_wall(curr_cell, next_cell)

                # append cell to the stack
                stack.append(next_cell)

    def draw(self, screen):
        # define colors
        black = (0, 0, 0)

        for cell in self.cells:
            x = cell.x * self.cell_size
            y = cell.y * self.cell_size

            wall = self.wall_t
            cels = self.cell_size

            wrec = cels + 2 * wall
            hrec = wall

            # wall rectangles
            rect_x = (x, y, cels, cels)
            rect_l = (x, y - wall, hrec, wrec)
            rect_r = (x + cels - wall, y - wall, hrec, wrec)
            rect_t = (x - wall, y, wrec, hrec)
            rect_b = (x - wall, y + cels - wall, wrec, hrec)

            # draw conditionally
            if not cell.visited:
                pygame.draw.rect(screen, black, rect_x)
                continue
            if cell.left:
                pygame.draw.rect(screen, black, rect_l)
            if cell.right:
                pygame.draw.rect(screen, black, rect_r)
            if cell.top:
                pygame.draw.rect(screen, black, rect_t)
            if cell.bottom:
                pygame.draw.rect(screen, black, rect_b)

    def save(self):
        # save in custom format
        with open("maze.custom", "wb") as outfile:
            outfile.write(bytes([self.width]))

            for cell in self.cells:
                wall_info = 0
                wall_info += cell.right << 0
                wall_info += cell.bottom << 1
                wall_info += cell.left << 2
                wall_info += cell.top << 3

                outfile.write(bytes([wall_info]))

    def load(self, path="maze.custom"):
        # load custom filetype
        self.cells.clear()

        with open(path, "rb") as infile:
            self.width = int.from_bytes(infile.read(1), "big")

            for i in range(self.width ** 2):
                wall_info = int.from_bytes(infile.read(1), "big")

                x = i % self.width
                y = int(i / self.width)

                cell = Cell(x, y)
                cell.right = wall_info & 0b0001
                cell.bottom = wall_info & 0b0010
                cell.left = wall_info & 0b0100
                cell.top = wall_info & 0b1000
                cell.visited = True

                self.cells.append(cell)
