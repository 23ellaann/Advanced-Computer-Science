import sys

import pygame
from pygame.locals import *

import random
import time
import numpy as np

pygame.init()

FPS = pygame.time.Clock()
FPS.tick(60)

BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

DISPLAY = pygame.display.set_mode((400, 550))
DISPLAY.fill(WHITE)

class Tile():
    def __init__(self, x, y):
        # 0 is unclicked, 1 is clicked, 2 is start/end, 3 is path
        self.status = 0
        self.x = x
        self.y = y


class Board():
    Tiles = []
    Rects = []
    startEnd = 0
    Maze = np.zeros((8, 8))

    def __init__(self, size):
        self.size = size
        pygame.display.set_caption("Game")
        Maze = np.zeros((size, size))
        self.startEnd = 0

    def setup(self):
        for i in range(self.size):
            arrayT = []
            arrayR = []
            for j in range(self.size):
                tile = Tile(50 * i + 3, 50 * j + 2)
                arrayT.append(tile)
                rect = pygame.draw.rect(DISPLAY, GREEN, pygame.Rect(tile.x, tile.y, 45, 45))
                arrayR.append(rect)
            self.Tiles.append(arrayT)
            self.Rects.append(arrayR)

    def click(self, x, y):
        tile = self.Tiles[x][y]
        if tile.status == 0:
            tile.status = 1
            rect = pygame.draw.rect(DISPLAY, RED, pygame.Rect(tile.x, tile.y, 45, 45))
            print("status 0")

        elif tile.status == 1:
            tile.status = 0
            rect = pygame.draw.rect(DISPLAY, GREEN, pygame.Rect(tile.x, tile.y, 45, 45))
            print("status 1")

    def clickStartEnd(self, x, y):
        tile = self.Tiles[x][y]
        if tile.status == 0 and self.startEnd < 2:
            tile.status = 2
            rect = pygame.draw.rect(DISPLAY, BLACK, pygame.Rect(tile.x, tile.y, 45, 45))
            print("status 2")
            self.startEnd += 1
        elif tile.status == 2:
            tile.status = 0
            rect = pygame.draw.rect(DISPLAY, GREEN, pygame.Rect(tile.x, tile.y, 45, 45))
            print("status 0")
            self.startEnd -= 1

    def maze(self):
        if self.startEnd == 2:
            startEndArray = []
            for i in range(self.size):
                for j in range(self.size):
                    if self.Tiles[i][j].status == 0:
                        self.Maze[i][j] = 0
                    elif self.Tiles[i][j].status == 1:
                        self.Maze[i][j] = 1
                    elif self.Tiles[i][j].status == 2:
                        tuple = (i, j)
                        startEndArray.append(tuple)

            start = startEndArray[0]
            end = startEndArray[1]
            path = astar(self.Maze, start, end)

            for i in path:
                rect = pygame.draw.rect(DISPLAY, BLUE, pygame.Rect(50 * i[0] + 3, 50 * i[1] + 3, 45, 45))
                self.Tiles[i[0]][i[1]] == 3
                print("status 3")
            return(path)


class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def astar(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]  # Return reversed path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:  # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (
                    len(maze[len(maze) - 1]) - 1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + (
                        (child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)


def main():
    board = Board(8)
    board.setup()

    while True:
        ev = pygame.event.get()

        for event in ev:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            x = -1
            for i in board.Rects:
                x = x + 1
                y = -1
                for j in i:
                    y += 1
                    for event in ev:
                        if event.type == pygame.KEYUP:
                            if event.key == 1073742049:
                                if board.Rects[x][y].collidepoint(pygame.mouse.get_pos()):
                                    board.click(x, y)
                            if event.key == 32:
                                board.maze()
                            if event.key == pygame.K_s or event.key == pygame.K_e:
                                if board.Rects[x][y].collidepoint(pygame.mouse.get_pos()):
                                    board.clickStartEnd(x, y)

        pygame.display.update()


if __name__ == '__main__':
    main()