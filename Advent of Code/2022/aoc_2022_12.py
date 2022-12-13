import heapq
from collections import deque
from dataclasses import dataclass
import numpy as np
import itertools
from math import inf

with open("aoc_2022_12.txt") as file:
    file_contents = [line.strip() for line in file]

NUM_ROWS = len(file_contents)
NUM_COLS = len(file_contents[0])

DIRECTIONS = ((1, 0),
              (0, 1),
              (-1, 0),
              (0, -1)
              )


def find_elevations(data):
    elev = dict()
    start_point = None
    finish_point = None
    for i, row in enumerate(data):
        for j, value in enumerate(row):
            if value == "S":
                start_point = (i, j)
                elev[(i, j)] = 0
            elif value == "E":
                finish_point = (i, j)
                elev[(i, j)] = 25
            else:
                elev[(i, j)] = ord(value) - ord('a')
    return elev, start_point, finish_point


@dataclass
class Node:
    # def __init__(self, location, height, parent=None):
    #     self.location = location
    #     self.height = height
    #     self.parent = parent
    location: tuple[int, int]
    height: int
    parent: object

    def find_unvisited_neighbours(self, elevation_map, visited):
        neighbours = []
        for d in DIRECTIONS:
            i, j = self.location[0] + d[0], self.location[1] + d[1]
            if ((0 <= i < NUM_ROWS) and
                    (0 <= j < NUM_COLS) and
                    (elevation_map[(i, j)] <= self.height + 1) and
                    ((i, j) not in visited)
            ):
                neighbours.append(Node((i, j), elevation_map[(i, j)], self))
        return neighbours


elevations, start, finish = find_elevations(file_contents)
start_node = Node(start, 0, None)
current_node = start_node

node_queue = deque()
visited = dict()

while current_node.location != finish:
    visited[current_node.location] = current_node
    for neighbour in current_node.find_unvisited_neighbours(elevations, visited.keys()):
        if neighbour.location not in visited:
            node_queue.append(neighbour)
    new_node = node_queue.popleft()
    if new_node.location not in visited:
        current_node = new_node
        print(current_node)

# finish = current_node
# path = []
#
# while current_node.parent:
#     path.append(current_node)
#     current_node = current_node.parent
#
# print(len(path))
