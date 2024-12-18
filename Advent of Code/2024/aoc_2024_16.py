from dataclasses import dataclass, field
from typing import Optional, Self
from queue import PriorityQueue
from collections import OrderedDict

with open("data/aoc_input_2024_16.txt") as file:
    file_contents = file.read()

# file_contents = """#################
# #...#...#...#..E#
# #.#.#.#.#.#.#.#.#
# #.#.#.#...#...#.#
# #.#.#.#.###.#.#.#
# #...#.#.#.....#.#
# #.#.#.#.#.#####.#
# #.#...#.#.#.....#
# #.#.#####.#.###.#
# #.#.#.......#...#
# #.#.###.#####.###
# #.#.#...#.....#.#
# #.#.#.#####.###.#
# #.#.#.........#.#
# #.#.#.#########.#
# #S#.............#
#################"""

# file_contents = """###############
# #.......#....E#
# #.#.###.#.###.#
# #.....#.#...#.#
# #.###.#####.#.#
# #.#.#.......#.#
# #.#.#####.###.#
# #...........#.#
# ###.#.#####.#.#
# #...#.....#.#.#
# #.#.#.###.#.#.#
# #.....#...#.#.#
# #.###.#.#.#.#.#
# #S..#.....#...#
# ###############"""

file_grid = file_contents.split("\n")
move_directions = {'W': (0, -1), 'N': (-1, 0), 'E': (0, 1), 'S': (1, 0)}
op_directions = {'W': 'E', 'N': 'S', 'E': 'W', 'S': 'N'}

@dataclass
class Grid:
    walls: set[tuple[int, int]] = field(default_factory=set)
    end: tuple[int, int] = (0,0)
    start: tuple[int, int] = (0,0)
    n_rows: int = 0
    n_cols: int = 0

    def read_grid(self, grid):
        for r, line in enumerate(grid):
            for c, character in enumerate(line):
                if character == "#":
                    self.walls.add((r, c))
                if character == "S":
                    self.start = (r, c)
                if character == "E":
                    self.end = (r, c)
        self.n_rows = len(grid)
        self.n_cols = len(grid[0])

    def exit_directions(self, pos, not_include=''):
        if pos in self.walls:
            exits = None
        else:
            neighbours = {direct: (pos[0] + dir_vec[0], pos[1] + dir_vec[1])
                          for direct, dir_vec in move_directions.items()}
            exits = {direct for direct, n_pos in neighbours.items() if n_pos not in self.walls} - set(not_include)
        return exits

@dataclass(frozen=True, order=True)
class Node:
    position: tuple[int, int]
    direction: str

    def find_neighbours(self, maze: Grid, starting_cost = 0):
        neighbours = {}
        n_paths = {}
        cur_cost = starting_cost
        for exit_dir in maze.exit_directions(self.position, op_directions[self.direction]):
            new_path = set()
            next_exit = exit_dir
            continue_path = True
            [cur_r, cur_c] = self.position
            cur_cost = starting_cost if (next_exit == self.direction) else starting_cost + 1000
            while continue_path:
                p, q = move_directions[next_exit]
                next_pos = (cur_r + p, cur_c + q)
                num_exits = len(maze.exit_directions(next_pos))
                # Reached branch or exit, store the node
                if num_exits > 2 or next_pos == maze.end:
                    cur_cost += 1
                    new_path.add(next_pos)
                    new_path |= paths[self]
                    neighbours[Node(next_pos, next_exit)] = (cur_cost, new_path)
                    continue_path = False
                # Dead end - only exit is the path you came from
                elif num_exits == 1:
                    continue_path = False
                # Only one exit, keep going
                elif num_exits == 2:
                    for e in maze.exit_directions(next_pos, not_include=op_directions[next_exit]):
                        # Increase cost by 1000 if change in direction required
                        if e != next_exit:
                            cur_cost += 1000
                        next_exit = e
                    cur_cost += 1
                    cur_r, cur_c = next_pos
                    new_path.add(next_pos)

        return neighbours


maze_grid = Grid()
maze_grid.read_grid(file_grid)
start = Node(maze_grid.start, 'E')

current_node = start
current_cost = 0
paths = {start: {start.position}}

visited = OrderedDict({start:0})
priority_queue = PriorityQueue()
max_cost = 10_000_000

while current_cost <= max_cost:
    neighbour_nodes = current_node.find_neighbours(maze_grid, current_cost)
    for nn, nn_data in neighbour_nodes.items():
        cost, path = nn_data
        if nn not in visited or visited[nn] == cost:
            priority_queue.put((cost, nn, path))

    if priority_queue.empty():
        print('failed to find exit')
        break
    current_cost, new_node, new_path = priority_queue.get()

    # If node is in visited at the same cost then consolidate the paths
    if new_node in visited and current_cost == visited[current_node]:
        current_node = new_node
        paths[current_node] |= new_path

    if new_node not in visited:
        current_node = new_node
        visited[current_node] = current_cost
        paths[current_node] = new_path

    if current_node.position == maze_grid.end:
        max_cost = current_cost



finish_nodes = {node for node in visited if node.position == maze_grid.end}
finish_node = finish_nodes.pop()

print(f'Solution to 16a is {visited[finish_node]}')
print(f'Solution to 16b is {len(paths[finish_node])}')