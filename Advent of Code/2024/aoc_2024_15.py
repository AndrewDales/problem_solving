from typing import Iterator
from dataclasses import dataclass, field
from itertools import chain

with open('data/aoc_input_2024_15.txt') as file:
    file_contents = file.read()

# file_contents = """##########
# #..O..O.O#
# #......O.#
# #.OO..O.O#
# #..O@..O.#
# #O#..O...#
# #O..O..O.#
# #.OO.O.OO#
# #....O...#
# ##########
#
# <vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
# vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
# ><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
# <<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
# ^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
# ^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
# >^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
# <><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
# ^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
# v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"""

# file_contents = """#######
# #...#.#
# #.....#
# #..OO@#
# #..O..#
# #.....#
# #######
#
# <vv<<^^<<^^"""

file_grid, file_directions = file_contents.split("\n\n")
file_grid = file_grid.split("\n")
file_directions = file_directions.replace("\n", "")

move_directions = {'<': (0, -1), '^': (-1, 0), '>': (0, 1), 'v': (1, 0)}

@dataclass
class Grid:
    directions: Iterator[str]
    walls: set[tuple[int, int]] = field(default_factory=set)
    rocks: set[tuple[int, int]] = field(default_factory=set)
    robot: tuple[int, int] = field(default=(0, 0))
    n_rows: int = 0
    n_cols: int = 0

    def read_grid(self, grid):
        for r, line in enumerate(grid):
            for c, character in enumerate(line):
                if character == "#":
                    self.walls.add((r, c))
                if character == "O":
                    self.rocks.add((r, c))
                if character == "@":
                    self.robot = (r, c)
        self.n_rows = len(grid)
        self.n_cols = len(grid[0])
        self.directions = iter(self.directions)

    def move_robot(self, direct):
        x, y = self.robot
        p, q = move_directions[direct]
        moving_rocks = []
        gathering_rocks = True
        move = True
        while gathering_rocks:
            x, y = x + p, y + q
            if (x, y) in self.rocks:
                moving_rocks.append((x,y))
            elif (x, y) in self.walls:
                move = False
                gathering_rocks = False
            else:
                gathering_rocks = False

        if move:
            if moving_rocks:
                self.rocks -= set(moving_rocks)
                self.robot = moving_rocks.pop(0)
                moving_rocks.append((x,y))
                self.rocks |= set(moving_rocks)
            else:
                self.robot = (x, y)

    def move_directions(self):
        for direction in self.directions:
            self.move_robot(direction)

    def calc_score(self):
        return sum(100 * r + c for r, c in self.rocks)

    def draw_grid(self):
        for r in range(self.n_rows):
            for c in range(self.n_cols):
                if (r, c) in self.walls:
                    print('#', end="")
                elif (r, c) in self.rocks:
                    print('O', end="")
                elif (r, c) == self.robot:
                    print('@', end="")
                else:
                    print('.', end='')
            print()


@dataclass
class GridEnlarged:
    directions: Iterator[str]
    walls: set[tuple[int, int]] = field(default_factory=set)
    crates: dict[int:tuple[tuple[int, int],tuple[int,int]]] = field(default_factory=dict)
    robot: tuple[int, int] = field(default=(0, 0))
    n_rows: int = 0
    n_cols: int = 0

    def read_grid(self, grid):
        i = 0
        for r, line in enumerate(grid):
            for c, character in enumerate(line):
                if character == "#":
                    self.walls.add((r, 2 * c))
                    self.walls.add((r, 2 * c + 1))
                if character == "O":
                    self.crates[i] = ((r, 2 * c), (r, 2 * c + 1))
                    i += 1
                if character == "@":
                    self.robot = (r, 2 * c)

        self.n_rows = len(grid)
        self.n_cols = len(grid[0]) * 2
        self.directions = iter(self.directions)

    @property
    def left_crate_sides(self):
        return {val[0]:key for key, val in self.crates.items()}

    @property
    def right_crate_sides(self):
        return {val[1]:key for key, val in self.crates.items()}

    @property
    def crate_sides(self):
        return self.left_crate_sides | self.right_crate_sides

    def draw_grid(self):
        for r in range(self.n_rows):
            for c in range(self.n_cols):
                if (r, c) in self.walls:
                    print('#', end="")
                elif (r, c) in self.left_crate_sides:
                    print('[', end="")
                elif (r, c) in self.right_crate_sides:
                    print(']', end="")
                elif (r, c) == self.robot:
                    print('@', end="")
                else:
                    print('.', end='')
            print()

    def crate_positions(self, index_list):
        return {pos for i in index_list for pos in self.crates[i]}

    def move_robot(self, direct):
        rob_x, rob_y = self.robot
        p, q = move_directions[direct]
        moving_crates = set()
        gathering_crates = True
        move = True
        new_positions = ((rob_x + p, rob_y + q),)
        while gathering_crates:
            if any(pos in self.walls for pos in new_positions):
                move = False
                gathering_crates = False
                break
            new_crates = {self.crate_sides[new_pos] for new_pos in new_positions if new_pos in self.crate_sides}
            if new_crates:
                if direct in '<>':
                    new_positions = ((new_positions[0][0] + p, new_positions[0][1] + 2 * q),)
                elif direct in '^v':
                    new_positions = tuple((r + p, s + q) for r, s in self.crate_positions(new_crates))

                moving_crates |= new_crates
            else:
                gathering_crates = False

        if move:
            for crate_num in moving_crates:
                left, right = self.crates[crate_num]
                left = left[0] + p, left[1] + q
                right = right[0] + p, right[1] + q
                self.crates[crate_num] = (left, right)
            self.robot = (rob_x + p, rob_y + q)

    def move_directions(self):
        for direction in self.directions:
            self.move_robot(direction)
            # print(f'Move = {direction}')
            # self.draw_grid()

    def calc_score(self):
        return sum(100 * r + c for r, c in self.left_crate_sides)

warehouse = Grid(iter(file_directions))
warehouse.read_grid(file_grid)
warehouse.move_directions()

print(f'Solution to Day 15a is {warehouse.calc_score()}')

big_warehouse = GridEnlarged(iter(file_directions))
big_warehouse.read_grid(file_grid)
big_warehouse.move_directions()

print(f'Solution to Day 15b is {big_warehouse.calc_score()}')