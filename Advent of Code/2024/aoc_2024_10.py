from dataclasses import dataclass, field

test_data = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""

with open('data/aoc_input_2024_10.txt') as file:
    file_contents = file.read()

# file_contents = test_data

file_data = file_contents.strip().split('\n')

@dataclass
class Grid:
    data: dict[tuple[int, int] : int] = field(default_factory=dict)
    n_rows: int = 0
    n_cols: int = 0

    def set_up(self, file_info):
        self.n_rows = len(file_info)
        self.n_cols = len(file_info[0])
        self.data = {(row, col): int(val) for row in range(self.n_rows) for col, val in enumerate(file_info[row])}

    def neighbours(self, pos):
        directions = ((-1, 0), (0, 1), (1, 0), (0, -1))
        r, c = pos
        return [(r + p, c + q) for p, q in directions
                if (0 <= r + p < self.n_rows and
                    0 <= c + q < self.n_cols)
                ]

    def trail_ends(self, pos, n=0):
        if self.data[pos] != n:
            return set()
        elif n == 9:
            return {pos}
        else:
            t_ends = set()
            ngh = self.neighbours(pos)
            for n_pos in ngh:
                t_ends = t_ends | self.trail_ends(n_pos, n + 1)
            return t_ends

    def trail_paths(self, pos, n=0):
        if self.data[pos] != n:
            return 0
        elif n == 9:
            return 1
        else:
            ngh = self.neighbours(pos)
            return sum(self.trail_paths(n_pos, n+1) for n_pos in ngh)


grid = Grid()
grid.set_up(file_data)
trail_ends = sum(len(grid.trail_ends(pos)) for pos in grid.data.keys())
trail_paths = sum(grid.trail_paths(pos) for pos in grid.data.keys())

print(f'Solution to Day 10a is {trail_ends}')
print(f'Solution to Day 10b is {trail_paths}')