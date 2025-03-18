from dataclasses import dataclass, field
from typing import Optional, Self, Dict, Tuple
from queue import PriorityQueue
from collections import OrderedDict
import time

with open("data/aoc_input_2024_20.txt") as file:
    file_contents = file.read().strip()
look_ahead = 100

# file_contents = """###############
# #...#...#.....#
# #.#.#.#.#.###.#
# #S#...#.#.#...#
# #######.#.#.###
# #######.#.#...#
# #######.#.###.#
# ###..E#...#...#
# ###.#######.###
# #...###...#...#
# #.#####.#.###.#
# #.#...#.#.#...#
# #.#.#.#.#.#.###
# #...#...#...###
# ###############"""
# look_ahead = 50

file_grid = file_contents.split("\n")
move_directions: dict[str, tuple[int, int]] = {'W': (0, -1), 'N': (-1, 0), 'E': (0, 1), 'S': (1, 0)}
op_directions = {'W': 'E', 'N': 'S', 'E': 'W', 'S': 'N'}

@dataclass
class Grid:
    walls: set[tuple[int, int]] = field(default_factory=set)
    end: tuple[int, int] = (0,0)
    start: tuple[int, int] = (0,0)
    track: list[tuple[int, int]] = field(default_factory=list)
    track_dict: dict[tuple[int,int]: int] = field(default_factory=dict)
    n_rows: int = 0
    n_cols: int = 0
    shortcuts: list[int] = field(default_factory=list)
    shortcuts_2: list[int] = field(default_factory=list)

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

    def exit_directions(self, pos, not_include=None):
        if not_include is None:
            not_include = ()
        exits = {nn for dir_vec in move_directions.values()
                if ((nn:= (pos[0] + dir_vec[0], pos[1] + dir_vec[1])) not in self.walls
                    and nn != not_include)}
        return exits

    def find_track_path(self):
        self.track = []
        self.track.append(self.start)
        current_cell = self.start
        previous_cell = self.start
        while current_cell != self.end:
            current_cell, previous_cell = self.exit_directions(current_cell, previous_cell).pop(), current_cell
            self.track.append(current_cell)
        self.track_dict = {pos: i for i, pos in enumerate(self.track)}


    def find_cell_shortcuts(self, pos):
        ngh_walls = {nn for dir_vec in move_directions.values()
                    if ((nn:= (pos[0] + dir_vec[0], pos[1] + dir_vec[1])) in self.walls and
                        0 < nn[0] < self.n_rows-1 and
                        0 < nn[1] < self.n_cols-1)
                     }
        return {s_pos for nw in ngh_walls for s_pos in self.exit_directions(nw, pos)
                if s_pos in self.track}


    def find_shortcuts(self):
        for i, pos in enumerate(self.track):
            for short_cut in self.find_cell_shortcuts(pos):
                if short_cut in self.track[i+look_ahead+2:]:
                    self.shortcuts.append(self.track_dict[short_cut] - i - 2)

    def find_cell_shortcuts_2(self, pos, track_num):
        future_track = set(self.track[track_num+look_ahead+2:])
        short_cuts = sum((self.track_dict[f_pos] - track_num - dist) >= look_ahead for f_pos in future_track
                               if 2 <= (dist:= abs(f_pos[0] - pos[0]) + abs(f_pos[1] - pos[1])) <= 20)
        return short_cuts

    def draw_grid(self):
        for r in range(self.n_rows):
            for c in range(self.n_cols):
                if (c, r) in self.walls:
                    print('#', end='')
                elif (c, r) == self.start:
                    print('S', end='')
                elif (c, r) == self.end:
                    print('E', end='')
                elif (c, r) in self.track:
                    print('@', end='')
                else:
                    print('.', end='')
            print()


racetrack = Grid()
racetrack.read_grid(file_grid)
racetrack.find_track_path()
racetrack.find_shortcuts()

print(f'Solution to 20a is {sum(sc >= 100 for sc in racetrack.shortcuts)}')

tic = time.time()
print(f'Solution to 20b is '
      f'{sum(racetrack.find_cell_shortcuts_2(pos, i) for i, pos in enumerate(racetrack.track[:-look_ahead]))}')
toc = time.time()
print(f'Time take {toc - tic} ms')