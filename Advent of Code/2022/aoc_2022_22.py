from dataclasses import dataclass, field
import re
from typing import Tuple

file_name = "aoc_2022_22.txt"

with open(file_name) as file:
    file_contents = file.read()

turns = re.findall(r'[LR]', file_contents)
moves = re.findall(r'[0-9]+', file_contents)
moves = [int(mv) for mv in moves]

file_lines = file_contents.split('\n')


@dataclass
class Map:
    floor: set[tuple[int, int]] = field(default_factory=set)
    wall: set[tuple[int, int]] = field(default_factory=set)

    def __post_init__(self):
        self.all_cells = self.floor | self.wall
        self.max_width = max(map_loc[1] for map_loc in self.all_cells)
        self.max_height = max(map_loc[0] for map_loc in self.all_cells)
        self.width_range = dict()
        self.height_range = dict()

        for row in range(1, self.max_height + 1):
            self.width_range[row] = (min(pos[1] for pos in self.all_cells if pos[0] == row),
                                     max(pos[1] for pos in self.all_cells if pos[0] == row),
                                     )
        for col in range(1, self.max_width + 1):
            self.height_range[col] = (min(pos[0] for pos in self.all_cells if pos[1] == col),
                                      max(pos[0] for pos in self.all_cells if pos[1] == col),
                                      )


class Map2(Map):
    def __init__(self, floor, wall, edge):
        super().__init__(floor, wall)
        self.edge = edge


floors = {(i, j) for i, line in enumerate(file_lines, 1) for j, mk in enumerate(line, 1) if mk == "."}
walls = {(i, j) for i, line in enumerate(file_lines, 1) for j, mk in enumerate(line, 1) if mk == "#"}

edges = dict()

# Test edges
if file_name == "aoc_2022_22_test.txt":
    for i in range(4):
        # Edge a
        edges[(i + 1, 9), 'W'] = (5, 5 + i), 'S'
        edges[(5, 5 + i), 'N'] = (i + 1, 9), 'E'
        # Edge b
        edges[(5, i + 1), 'N'] = (1, 12 - i), 'S'
        edges[(1, 12 - i), 'N'] = (5, i + 1), 'S'
        # Edge c
        edges[(5 + i, 12), 'E'] = (9, 16 - i), 'S'
        edges[(9, 16 - i), 'N'] = (5 + i, 12), 'W'
        # Edge d
        edges[(1 + i, 12), 'E'] = (12 - i, 16), 'W'
        edges[(12 - i, 16), 'E'] = (i + 1, 12), 'W'
        # Edge e
        edges[(8, 5 + i), 'S'] = (12 - i, 9), 'E'
        edges[(12 - i, 9), 'W'] = (8, 5 + i), 'N'
        # Edge f
        edges[(8, 1 + i), 'S'] = (12, 12 - i), 'N'
        edges[(12, 12 - i), 'S'] = (8, 1 + i), 'N'
        # Edge g
        edges[(1, 5 + i), 'W'] = (12, 16 - i), 'N'
        edges[(12, 16 - i), 'S'] = (1, 5 + i), 'E'

elif file_name == "aoc_2022_22.txt":
    for i in range(50):
        # Edge a
        edges[(1, 51 + i), 'N'] = (151 + i, 1), 'E'
        edges[(151 + i, 1), 'W'] = (1, 51 + i), 'S'
        # Edge b
        edges[(1, 101 + i), 'N'] = (200, 1 + i), 'N'
        edges[(200, 1 + i), 'S'] = (1, 101 + i), 'S'
        # Edge c
        edges[(101 + i, 1), 'W'] = (50 - i, 51), 'E'
        edges[(50 - i, 51), 'W'] = (101 + i, 1), 'E'
        # Edge d
        edges[(51 + i, 51), 'W'] = (101, 1 + i), 'S'
        edges[(101, 1 + i), 'N'] = (51 + i, 51), 'E'
        # Edge e
        edges[(1 + i, 150), 'E'] = (150 - i, 100), 'W'
        edges[(150 - i, 100), 'E'] = (1 + i, 150), 'W'
        # Edge f
        edges[(51 + i, 100), 'E'] = (50, 101 + i), 'N'
        edges[(50, 101 + i), 'S'] = (51 + i, 100), 'W'
        # Edge g
        edges[(150, 51 + i), 'S'] = (151 + i, 50), 'W'
        edges[(151 + i, 50), 'E'] = (150, 51 + i), 'N'


monkey_map = Map(floors, walls)
monkey_map_2 = Map2(floors, walls, edges)


@dataclass
class Path:
    position: tuple[int, int]
    map: Map | Map2
    facing: str = "E"
    directions: list[str] = field(default_factory=lambda: list("NESW"))

    def turn(self, direction):
        facing_num = self.directions.index(self.facing)
        if direction == "R":
            facing_num = (facing_num + 1) % len(self.directions)
        elif direction == "L":
            facing_num = (facing_num - 1) % len(self.directions)
        self.facing = self.directions[facing_num]

    def move_once(self):
        new_position = list(self.position)
        moved = None
        if self.facing == "S":
            new_position[0] += 1
            if new_position[0] > self.map.height_range[self.position[1]][1]:
                new_position[0] = self.map.height_range[self.position[1]][0]
        elif self.facing == "N":
            new_position[0] -= 1
            if new_position[0] < self.map.height_range[self.position[1]][0]:
                new_position[0] = self.map.height_range[self.position[1]][1]
        elif self.facing == "E":
            new_position[1] += 1
            if new_position[1] > self.map.width_range[self.position[0]][1]:
                new_position[1] = self.map.width_range[self.position[0]][0]
        elif self.facing == "W":
            new_position[1] -= 1
            if new_position[1] < self.map.width_range[self.position[0]][0]:
                new_position[1] = self.map.width_range[self.position[0]][1]
        if tuple(new_position) in self.map.floor:
            self.position = tuple((new_position[0], new_position[1]))
            moved = True
        elif tuple(new_position) in self.map.wall:
            moved = False
        return moved

    def move(self, distance):
        for _ in range(distance):
            mv = self.move_once()
            if not mv:
                break

    def move_sequence(self, p_moves, p_turns):
        p_turns.append("")
        for mv, tn in zip(p_moves, p_turns):
            self.move(mv)
            self.turn(tn)

    def position_score(self):
        facing_scores = {"E": 0, "S": 1, "W": 2, "N": 3}
        return self.position[0] * 1000 + self.position[1] * 4 + facing_scores[self.facing]


class Path2(Path):
    def move_once(self):
        moved = None
        if (self.position, self.facing) in self.map.edge:
            new_position, new_facing = self.map.edge[(self.position, self.facing)]
        else:
            new_position = list(self.position)
            new_facing = self.facing
            if self.facing == "S":
                new_position[0] += 1
            elif self.facing == "N":
                new_position[0] -= 1
            elif self.facing == "E":
                new_position[1] += 1
            elif self.facing == "W":
                new_position[1] -= 1

        if tuple(new_position) in self.map.floor:
            self.position = tuple((new_position[0], new_position[1]))
            self.facing = new_facing
            moved = True
        elif tuple(new_position) in self.map.wall:
            moved = False
        return moved


start_i = 1
start_j = min(pos[1] for pos in monkey_map.floor if pos[0] == 1)

monkey_path = Path(position=(start_i, start_j), map=monkey_map)
monkey_path.move_sequence(moves, turns)

print(f'Solution to Day 22, Part 1 is {monkey_path.position_score()}')

monkey_path_2 = Path2(position=(start_i, start_j), map=monkey_map_2)
monkey_path_2.move_sequence(moves, turns)

# Checks a
my_path = Path2(position=(1, 55), facing='N', map=monkey_map_2)
my_path.move_once()
assert my_path.position == (155, 1)
assert my_path.facing == 'E'

# Check b
my_path = Path2(position=(1, 110), facing='N', map=monkey_map_2)
my_path.move_once()
assert my_path.position == (200, 10)
assert my_path.facing == 'N'

# Check c
my_path = Path2(position=(10, 51), facing='W', map=monkey_map_2)
my_path.move_once()
assert my_path.position == (141, 1)
assert my_path.facing == 'E'

# Check d
my_path = Path2(position=(59, 51), facing='W', map=monkey_map_2)
my_path.move_once()
assert my_path.position == (101, 9)
assert my_path.facing == 'S'

# Check e
my_path = Path2(position=(4, 150), facing='E', map=monkey_map_2)
my_path.move_once()
assert my_path.position == (147, 100)
assert my_path.facing == 'W'

# Check f
my_path = Path2(position=(98, 100), facing='E', map=monkey_map_2)
my_path.move_once()
assert my_path.position == (50, 148)
assert my_path.facing == 'N'


print(f'Solution to Day 22, Part 2 is {monkey_path_2.position_score()}')