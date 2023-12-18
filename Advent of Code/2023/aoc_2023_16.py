import re
from dataclasses import dataclass

with open('data/aoc_input_2023_16.txt') as file:
    file_contents = [line.strip() for line in file.readlines()]


def parse_contraption(contraption_lines):
    cells = dict()
    for row, line in enumerate(contraption_lines):
        matches = re.finditer(r'[\|\\/-]', line)
        cells.update({(row, m.start()): m.group() for m in matches})
    return cells


@dataclass(frozen=True)
class Beam:
    location: tuple[int, int]
    direction: str


class Path:
    directions = {'N': (-1, 0),
                  'E': (0, 1),
                  'S': (1, 0),
                  'W': (0, -1),
                  }
    mirror_dirs = {'/': {'E': 'N', 'W': 'S', 'S': 'W', 'N': 'E'},
                   '\\': {'E': 'S', 'W': 'N', 'S': 'E', 'N': 'W'},
                   '|': {'N': 'N', 'S': 'S', 'E': 'NS', 'W': 'NS'},
                   '-': {'N': 'EW', 'S': 'EW', 'E': 'E', 'W': 'W'},
                   }

    def __init__(self, contraption_mirrors, rows, columns):
        self.mirrors = contraption_mirrors
        self.dims = (rows, columns)
        self.current_beam = None
        self.beam_stack = []
        self.visited = set()
        self.energized = set()

    def outside_grid(self, location):
        inside = 0 <= location[0] < self.dims[0] and 0 <= location[1] < self.dims[1]
        return not inside

    def track_beam(self, start: Beam):
        self.current_beam = start
        self.beam_stack = []
        self.visited = set()
        self.energized = set()
        finished_tracking = False
        while not finished_tracking:
            self.move_beam()
            if self.beam_stack:
                self.current_beam = self.beam_stack.pop()
            else:
                finished_tracking = True
        return len(self.energized)

    def move_beam(self):
        end_beam = False
        move = self.directions[self.current_beam.direction]
        next_location = (self.current_beam.location[0] + move[0], self.current_beam.location[1] + move[1])
        # move outside the grid
        if self.outside_grid(next_location):
            end_beam = True
        else:
            if next_location in self.mirrors:
                current_mirror = self.mirrors[next_location]
                new_directions = self.mirror_dirs[current_mirror][self.current_beam.direction]
                new_beam = Beam(next_location, direction=new_directions[0])
                # Splitter - add split beam to beam stack
                if len(new_directions) > 1:
                    self.beam_stack.append(Beam(next_location, direction=new_directions[1]))
                # Check if same location and direction has already been visited
                if new_beam in self.visited:
                    end_beam = True
            else:
                new_beam = Beam(next_location, self.current_beam.direction)

            self.current_beam = new_beam
            self.visited.add(new_beam)
            self.energized.add(new_beam.location)
        if not end_beam:
            self.move_beam()
        return


n_rows = len(file_contents)
n_cols = len(file_contents)
# n_rows = len(contraption_string) // n_cols
#
mirrors = parse_contraption(file_contents)
beam_path = Path(mirrors, n_rows, n_cols)

print(f'Solution to Part 1 is {beam_path.track_beam(Beam((0, -1), "E"))}')

starting_points = ([Beam((i, -1), "E") for i in range(n_rows)] +
                   [Beam((i, n_cols), "W") for i in range(n_rows)] +
                   [Beam((-1, i), "S") for i in range(n_cols)] +
                   [Beam((n_rows, i), "N") for i in range(n_cols)]
                   )

tiles_energized = [beam_path.track_beam(start_beam) for start_beam in starting_points]

print(f'Solution to Part 2 is {max(tiles_energized)}')
