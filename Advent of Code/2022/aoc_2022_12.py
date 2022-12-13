from collections import deque
from dataclasses import dataclass

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
    distance: int = 0

    def find_unvisited_neighbours(self, elevation_map, p_visited, reverse=False):
        neighbours = []
        for d in DIRECTIONS:
            i, j = self.location[0] + d[0], self.location[1] + d[1]
            if not ((0 <= i < NUM_ROWS) and 0 <= j < NUM_COLS):
                continue

            if reverse:
                height_condition = (elevation_map[(i, j)] >= self.height - 1)
            else:
                height_condition = (elevation_map[(i, j)] <= self.height + 1)

            if height_condition and (i, j) not in p_visited:
                neighbours.append((i, j))
        return neighbours


elevations, start, finish = find_elevations(file_contents)
start_node = Node(location=start, height=0, parent=None, distance=0)
current_node = start_node

node_queue = deque()
node_directory = {start: start_node}
visited = set()

while current_node.location != finish:
    visited.add(current_node.location)
    for neighbour in current_node.find_unvisited_neighbours(elevations, node_directory):
        node_queue.append(neighbour)
        node_directory[neighbour] = Node(location=neighbour,
                                         height=elevations[neighbour],
                                         parent=current_node,
                                         distance=current_node.distance + 1)
    new_location = node_queue.popleft()
    if new_location not in visited:
        current_node = node_directory[new_location]
        # print(current_node.location)

finish_node = current_node

print(f'Solution to part 1 = {finish_node.distance}')

finish_node.parent = None
finish_node.distance = 0
node_queue = deque()
node_directory = {finish: finish_node}
visited = set()

while current_node.height != 0:
    visited.add(current_node.location)
    for neighbour in current_node.find_unvisited_neighbours(elevations, node_directory, reverse=True):
        node_queue.append(neighbour)
        node_directory[neighbour] = Node(location=neighbour,
                                         height=elevations[neighbour],
                                         parent=current_node,
                                         distance=current_node.distance + 1)
    new_location = node_queue.popleft()
    if new_location not in visited:
        current_node = node_directory[new_location]

print(f'Solution to part 2 = {current_node.distance}')

path = []

while current_node.parent:
    path.append((current_node.location, current_node.height))
    current_node = current_node.parent
