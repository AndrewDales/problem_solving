from dataclasses import dataclass, field
from collections import defaultdict
from itertools import combinations
import re

with open('data/aoc_input_2024_8.txt') as file:
    file_contents = file.read()

@dataclass
class Grid:
    antenna: defaultdict[str: list[tuple]] = field(default_factory=lambda: defaultdict(list))
    anti_nodes: set[tuple[int, int]] = field(default_factory=set)
    num_rows: int = 0
    num_cols: int = 0

    def read_data(self, file_string):
        self.num_rows = file_string.index('\n')
        self.num_cols = file_string.count('\n')
        file_string = file_string.replace("\n", "")
        antenna_matches = re.finditer(r'\w', file_string)
        for m in antenna_matches:
            key = m.group()
            pos = divmod(m.span()[0], self.num_rows)
            self.antenna[key].append(pos)

    @staticmethod
    def find_anti_node_coords(pos_1, pos_2, rows=50, cols=50, puzzle=1):
        def find_check(a, b, dist = 2):
            node_added = False
            i, j = dist * a[0] - (dist-1) * b[0], dist * a[1] - (dist-1) * b[1]
            if 0 <= i < rows and 0 <= j < cols:
                nodes.append((i, j))
                node_added = True
            return node_added

        nodes = []
        if puzzle==1:
            find_check(pos_1, pos_2, 2)
            find_check(pos_2, pos_1, 2)
        else:
            d = 1
            while find_check(pos_1, pos_2, d):
                d += 1
            d = 1
            while find_check(pos_2, pos_1, d):
                d += 1
        return nodes

    def find_anti_nodes(self, puzzle=1):
        for key, pos_list in self.antenna.items():
            a_nodes = (self.find_anti_node_coords(a, b, self.num_rows, self.num_cols, puzzle)
                            for a,b in combinations(pos_list, 2))
            self.anti_nodes.update(*a_nodes)


grid = Grid()
grid.read_data(file_contents)
grid.find_anti_nodes(puzzle=1)

print(f'Solution to Advent of Code Day 8a is {len(grid.anti_nodes)}')

grid.anti_nodes.clear()
grid.find_anti_nodes(puzzle=2)

print(f'Solution to Advent of Code Day 8b is {len(grid.anti_nodes)}')