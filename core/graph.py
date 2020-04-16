"""
GRAPH CLASS
"""

import pygame
import random


class Node:
    def __init__(self, x, y):
        # coords
        self.x = x
        self.y = y

        # parent
        self.parent = None

    def addattr_dirs(self):
        # for all directions
        self.right = None
        self.left = None
        self.bottom = None
        self.top = None

    def delattr_dirs(self):
        # delete directions
        del self.right
        del self.left
        del self.bottom
        del self.top


class Graph:
    def __init__(self, width, cell_size=20):
        # params
        self.width = width
        self.cell_size = cell_size

        # node list
        self.nodes = []

    def get(self, x, y):
        # obtain first match
        for node in self.nodes:
            if node.x == x and node.y == y:
                return node

        return None

    def delete(self, x, y):
        # delete first match
        self.nodes.remove(self.get(x, y))

    def convert_from_cells(self, maze):
        # initialize temp_node list
        temp_nodes = []

        # convert to nodes
        for cell in maze.cells:
            # current node init
            current = Node(cell.x, cell.y)
            current.addattr_dirs()

            # horizontal connections
            if not cell.left:
                lnode = self.get(cell.x - 1, cell.y)
                current.left = lnode.left if lnode in temp_nodes else lnode
                current.left.right = current

            # vertical connections
            if not cell.top:
                tnode = self.get(cell.x, cell.y - 1)
                current.top = tnode.top if tnode in temp_nodes else tnode
                current.top.bottom = current

            # decide if the node is temp
            h_cond = cell.top and cell.bottom and not (cell.right or cell.left)
            v_cond = cell.right and cell.left and not (cell.top or cell.bottom)

            # append to temp_node list
            nodestat = current if h_cond or v_cond else None
            temp_nodes.append(nodestat)

            # add current node to list
            self.nodes.append(current)

        # filter temp nodes
        self.nodes = list(filter(lambda x: x not in temp_nodes, self.nodes))

    def solve_dijkstra(self, init_pos, dest_pos):
        # define infinity
        infinity = 10 ** 9

        # unpack x, y values
        init_x, init_y = init_pos
        dest_x, dest_y = dest_pos

        # get node data
        init_node = self.get(init_x, init_y)
        dest_node = self.get(dest_x, dest_y)

        # invalid node condition
        if init_node is None or dest_node is None:
            print("\033[31mError : \033[0m", end="")
            print("node coordinates invalid")
            return

        # add attributes for solving
        for node in self.nodes:
            setattr(node, "done", False)
            setattr(node, "dist", infinity)

        # initial conditions
        current = init_node
        current.dist = 0

        # function to get distance
        node_dist = lambda x1, x2: abs(x1.x - x2.x) + abs(x1.y - x2.y)

        # loop until destination node gets done
        while not dest_node.done:
            # get min value from incomplete
            incomplete = list(filter(lambda x: not x.done, self.nodes))
            current = min(incomplete, key=lambda x: x.dist) 

            # list all children and filter them
            children = [current.right, current.bottom, current.left, current.top]
            children = list(filter(lambda x: x is not None and not x.done, children))

            # iterate through all sides
            for child_node in children:
                # find if the path through current is the best
                new_dist = current.dist + node_dist(current, child_node)

                # update if better path found
                if new_dist < child_node.dist:
                    child_node.parent = current
                    child_node.dist = new_dist

            # set current as done
            current.done = True                       

        # remove attributes used for solving
        for node in self.nodes:
            delattr(node, "done")
            delattr(node, "dist")

    def draw(self, screen):
        # draw all nodes and connections

        # colors
        dot_col = (0, 0, 255)
        line_col = (250, 20, 20)

        # short variables
        cels = self.cell_size
        offset = int(cels * 0.5)
        node_rad = int(cels * 0.2)

        # drawing on screen
        for node in self.nodes:
            # nodes
            center = (node.x * cels + offset, node.y * cels + offset)
            pygame.draw.circle(screen, dot_col, center, node_rad)

            # top connection
            if node.top is not None:
                tcenter = (node.top.x * cels, node.top.y * cels)
                tcenter = tuple([elem + offset for elem in tcenter])
                pygame.draw.line(screen, line_col, center, tcenter, 2)

            # left connection
            if node.left is not None:
                lcenter = (node.left.x * cels, node.left.y * cels)
                lcenter = tuple([elem + offset for elem in lcenter])
                pygame.draw.line(screen, line_col, center, lcenter, 2)

    def draw_solution(self, screen, dest_pos, line_t=2):
        # draw solution nodes and connections

        # colors
        dot_col = (0, 0, 255)
        line_col = (250, 20, 20)

        # short variables
        cels = self.cell_size
        offset = int(cels * 0.5)
        node_rad = int(cels * 0.2)

        # start from lowest level
        dest_x, dest_y = dest_pos
        current = self.get(dest_x, dest_y)

        # find validity
        if current is None:
            print("\033[32mError : \033[0m", end="")
            print("invalid destination")

        # the root node has no parent
        while current.parent is not None:
            # center
            center = (current.x * cels + offset, current.y * cels + offset)
            pygame.draw.circle(screen, dot_col, center, node_rad)

            # parent connection
            pcenter = (current.parent.x * cels, current.parent.y * cels)
            pcenter = tuple([elem + offset for elem in pcenter])
            pygame.draw.line(screen, line_col, center, pcenter, line_t)

            # update current
            current = current.parent
        
        # draw root node
        center = (current.x * cels + offset, current.y * cels + offset)
        pygame.draw.circle(screen, dot_col, center, node_rad)
