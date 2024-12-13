from dataclasses import dataclass, field
import copy

test_data = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""

with open('data/aoc_input_2024_6.txt') as file:
    file_contents = file.read()

# file_contents = test_data

file_contents = file_contents.splitlines()

DIRECTIONS = {'N': (-1, 0),
              'E': (0, 1),
              'S': (1, 0),
              'W': (0, -1)}

NEXT_LOCATION = {'N': 'E',
              'E': 'S',
              'S': 'W',
              'W': 'N'}

@dataclass
class Map:
    blocks: set[tuple[int, int]] = field(default_factory=set)
    guard_position: tuple[int, int, str] = field(default_factory=tuple)
    guard_path: list[tuple[int, int, str]] = field(default_factory=list)
    num_rows: int = 0
    num_cols: int = 0
    status: str = 'moving'

    def read_data(self, map_text):
        self.num_rows = len(map_text)
        self.num_cols = len(map_text[0])
        for row, line in enumerate(map_text):
            for col, char in enumerate(line):
                if char == '#':
                    self.blocks.add((row, col))
                if char == '^':
                    self.guard_position = (row, col, 'N')
        self.guard_path.append(self.guard_position)

    def move_guard(self):
        dir_vec = DIRECTIONS[self.guard_position[2]]
        next_cell = self.guard_position[0] + dir_vec[0], self.guard_position[1] + dir_vec[1]
        # Hits block
        if next_cell in self.blocks:
            guard_dir = NEXT_LOCATION[self.guard_position[2]]
            self.guard_position = self.guard_position[:2] + (guard_dir, )
            if self.guard_position in self.guard_path:
                self.status = 'loop'
            self.guard_path.append(self.guard_position)
        # Moves out of grid
        elif not (0 <= next_cell[0] < self.num_rows and 0 <= next_cell[1] < self.num_cols):
            self.status = 'out'
        # Moves forward
        else:
            self.guard_position = next_cell + (self.guard_position[2], )
            self.guard_path.append(self.guard_position)


    def find_exit(self):
        while self.status == 'moving':
            self.move_guard()
        return self.status


initial_map = Map()
initial_map.read_data(file_contents)

# test_block(copy.deepcopy(initial_map), (1, 6))

puzzle_map = copy.deepcopy(initial_map)
puzzle_map.find_exit()
number_of_positions = len({(i, j) for i, j, _ in puzzle_map.guard_path})

print(f'Solution to Day 6a is {number_of_positions}')


loop_locations = []
for block_location in {(i, j) for i, j, _ in puzzle_map.guard_path}:
    test_map = copy.deepcopy(initial_map)
    test_map.blocks.add(block_location)
    exit_status = test_map.find_exit()
    if exit_status == 'loop':
        loop_locations.append(block_location)

print(f'Solution to Day 6b is {len(loop_locations)}')
