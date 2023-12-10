import re
from dataclasses import dataclass

with open("data/aoc_input_2023_10.txt") as file:
    file_contents = file.read()


@dataclass
class Cell:
    location: tuple[int, int]
    symbol: str

    @staticmethod
    def parse_match(match):
        symbol = match.group()
        col = match.start() // NUM_COLS
        row = match.start() % NUM_COLS
        if symbol == '.':
            cell = Cell((col, row), symbol)
        elif symbol == 'S':
            cell = StartPipePiece((col, row), symbol)
        else:
            cell = PipePiece((col, row), symbol)
        return cell

    @property
    def neighbours(self):
        return set((self.location[0] + d[0], self.location[1] + d[1])
                   for d in DIRECTIONS.values())


class PipePiece(Cell):
    def pipe_neighbours(self):
        return [(self.location[0] + d[0], self.location[1] + d[1])
                for d in [DIRECTIONS[cd] for cd in CONNECTIONS[self.symbol]]]


class StartPipePiece(PipePiece):
    def pipe_neighbours(self):
        # nghs = [(self.location[0] + d[0], self.location[1] + d[1])
        #         for d in DIRECTIONS.values()]
        nghs = [n for n in self.neighbours
                if n in pipes and self.location in pipes[n].pipe_neighbours()]
        return nghs


NUM_COLS = file_contents.find('\n')
DIRECTIONS = {'N': (-1, 0), 'E': (0, 1), 'S': (1, 0), 'W': (0, -1)}
CONNECTIONS = {'|': 'NS',
               '-': 'EW',
               'L': 'NE',
               'J': 'NW',
               '7': 'SW',
               'F': 'SE',
               }
INNER_DIRECTIONS = {(1, 0): [(0, 1), (-1, 1)],
                    (0, 1): [(-1, 0), (-1, -1)],
                    (-1, 0): [(0, -1), (1, -1)],
                    (0, -1): [(1, 0), (1, 1)],
                    }

file_contents = file_contents.replace('\n', '')

symbol_search = re.finditer(r'[\S]', file_contents)
cells = dict()
for p in [Cell.parse_match(s_match) for s_match in symbol_search]:
    cells[p.location] = p
pipes = {k: v for k, v in cells.items() if isinstance(cells[k], PipePiece)}

start_pipe = [pipe for pipe in pipes.values() if pipe.symbol == 'S'][0]

pipe_path = [start_pipe.location,
             start_pipe.pipe_neighbours()[1]
             ]
previous_pipe, current_pipe = start_pipe, pipes[pipe_path[-1]]
potential_insides = set()

while current_pipe.symbol != 'S':
    nghs = current_pipe.pipe_neighbours()
    nghs.remove(pipe_path[-2])
    previous_pipe, current_pipe = current_pipe, pipes[nghs[0]]
    direction = (current_pipe.location[0] - previous_pipe.location[0],
                 current_pipe.location[1] - previous_pipe.location[1],
                 )
    inner_direction = INNER_DIRECTIONS[direction]
    pot_inside = {(current_pipe.location[0] + d[0],
                   current_pipe.location[1] + d[1],
                   ) for d in inner_direction
                  }
    potential_insides |= pot_inside
    # print(current_pipe, pot_inside)
    pipe_path.append(current_pipe.location)

print(f'Solution to Day 10, Part 1 is {len(pipe_path) // 2}')
pipe_path_set = set(pipe_path)

insides = potential_insides - pipe_path_set

all_insides = set()
insides_groups = []

while insides:
    inside_member = insides.pop()
    group = {inside_member}
    group_neighbours = cells[inside_member].neighbours - pipe_path_set
    while group_neighbours:
        inside_member = group_neighbours.pop()
        group.add(inside_member)
        group_neighbours = (group_neighbours | cells[inside_member].neighbours) - pipe_path_set - group
    insides -= group
    all_insides |= group

print(f'Solution to Day 10, Part 2 is {len(all_insides)}')

with open('data/aoc_output_2023_10.txt', 'w') as file:
    for i in range(140):
        for j in range(140):
            if (i, j) in pipe_path_set:
                file.write('#')
            elif (i, j) in all_insides:
                file.write('I')
            else:
                file.write('.')
        file.write('\n')
