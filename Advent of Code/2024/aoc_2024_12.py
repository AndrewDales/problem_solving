from  dataclasses import dataclass, field

with open('data/aoc_input_2024_12.txt') as file:
    file_contents = file.read()

# file_contents = """RRRRIICCFF
# RRRRIICCCF
# VVRRRCCFFF
# VVRCCCJFFF
# VVVVCJJCFE
# VVIVCCJJEE
# VVIIICJJEE
# MIIIIIJJEE
# MIIISIJEEE
# MMMISSJEEE"""

file_data = file_contents.strip().split('\n')

def neighbours(pos, rows, cols, directions=None):
    if directions is None:
        directions = ((-1, 0), (0, 1), (1, 0), (0, -1))
    r, c = pos
    return [(r + p, c + q) for p, q in directions
            if (rows[0] <= r + p < rows[1] and
                cols[0] <= c + q < cols[1])
            ]


class Region:
    def __init__(self, grid, pos):
        self.grid: 'Grid' = grid
        self.pos: tuple[int, int] = pos
        self.symbol: str = self.grid.data[pos]
        self.cells: set[tuple[int, int]] = {pos}
        self.find_region(pos)
        self.edges = self.find_edges()
        self.sides = self.find_sides()

    def find_region(self, pos):
        neighs = neighbours(pos, (0, self.grid.n_rows), (0, self.grid.n_cols))
        for n_pos in neighs:
            if self.grid.data[n_pos] == self.symbol and n_pos not in self.cells:
                self.cells.add(n_pos)
                self.find_region(n_pos)

    def find_edges(self):
        edges = set()
        directions = {'N':(-1, 0), 'E': (0, 1), 'S': (1, 0), 'W':(0, -1)}
        for pos in self.cells:
            for dir_letter, dir_v in directions.items():
                n_pos = (pos[0] + dir_v[0], pos[1] + dir_v[1])
                if n_pos not in self.cells:
                    edges.add(Edge(pos, dir_letter))
        return edges

    def find_sides(self):
        def add_neighbours(edge, side=None):
            if side is None:
                side = []

            self.edges.remove(edge)
            side.append(edge)
            for n_edge in edge.neighbours():
                if n_edge in self.edges:
                    add_neighbours(n_edge, side)
            return side

        sides = []
        while self.edges:
            new_edge = list(self.edges)[0]
            sides.append(add_neighbours(new_edge))
        return sides

    @property
    def area(self):
        return len(self.cells)

    @property
    def perimeter(self):
        perimeter_length = 0
        for pos in self.cells:
            neighs = neighbours(pos, (-1, self.grid.n_rows + 1), (-1, self.grid.n_cols + 1))
            for n_pos in neighs:
                if n_pos not in self.cells:
                    perimeter_length += 1
        return perimeter_length

    @property
    def price(self):
        return self.area * self.perimeter

    def price_sides(self):
        return self.area * len(self.sides)


@dataclass(frozen=True)
class Edge:
    cell: tuple[int, int]
    side: str

    def neighbours(self):
        r, c = self.cell
        if self.side in ('N', 'S'):
            neighs = (Edge((r, c - 1), self.side), Edge((r, c + 1), self.side))
        elif self.side in ('E','W'):
            neighs = (Edge((r - 1, c), self.side), Edge((r + 1, c), self.side))
        else:
            neighs = None
        return neighs


@dataclass
class Grid:
    data: dict[tuple[int, int] : str] = field(default_factory=dict)
    n_rows: int = 0
    n_cols: int = 0
    visited_cells: set[tuple[int, int]] = field(default_factory=set)
    regions: list[Region] = field(default_factory=list)

    def set_up(self, file_info):
        self.n_rows = len(file_info)
        self.n_cols = len(file_info[0])
        self.data = {(row, col): val for row in range(self.n_rows) for col, val in enumerate(file_info[row])}

    def find_regions(self):
        for pos in self.data:
            if pos not in self.visited_cells:
                reg = Region(self, pos)
                self.regions.append(reg)
                self.visited_cells.update(reg.cells)

    def find_score(self):
        return sum(reg.price for reg in self.regions), sum(reg.price_sides() for reg in self.regions)

full_grid = Grid()
full_grid.set_up(file_data)
full_grid.find_regions()

prices = full_grid.find_score()

print(f'Solution to Day 12a is {prices[0]}')
print(f'Solution to Day 12a is {prices[1]}')
