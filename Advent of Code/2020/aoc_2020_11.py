import numpy as np
import itertools
from math import inf
from dataclasses import dataclass

with open("aoc_2020_11.txt", "r") as file:
    seat_layout = [list(line.strip()) for line in file]

FLOOR = "."
EMPTY = "L"
OCCUPIED = "#"


def find_neighbours(cell, max_vals=None, min_vals=None, include_self=False):
    if min_vals is None:
        min_vals = [0] * len(cell)
    if max_vals is None:
        max_vals = [inf] * len(cell)

    ranges = [range(max(val - 1, min_vals[i]), min(val + 1, max_vals[i]) + 1) for i, val in enumerate(cell)]
    neighbours = {tuple(prd) for prd in itertools.product(*ranges)}
    if not include_self:
        neighbours.remove(cell)
    return neighbours


@dataclass
class SeatState:
    layout: dict
    problem: int = 1

    def __post_init__(self):
        self.size = max(self.layout.keys())
        if self.problem == 2:
            self.max_occupied = 5
        else:
            self.max_occupied = 4

    @classmethod
    def parse_plan(cls, plan, prob):
        return SeatState({(i, j): symbol
                          for i, row in enumerate(plan)
                          for j, symbol in enumerate(row)},
                         problem=prob)

    def transition_layout(self):
        return SeatState({cell: self.change_status(cell) for cell in self.layout}, problem=self.problem)

    def change_status(self, cell):
        new_status = self.layout[cell]
        if new_status in (EMPTY, OCCUPIED):
            if self.problem == 2:
                neighbours = self.find_seen_neighbours(cell)
            else:
                neighbours = find_neighbours(cell, max_vals=self.size)

            n_occ_neighbours = sum(True for ngh in neighbours if self.layout[ngh] == OCCUPIED)
            if new_status == EMPTY and n_occ_neighbours == 0:
                new_status = OCCUPIED
            elif new_status == OCCUPIED and n_occ_neighbours >= self.max_occupied:
                new_status = EMPTY
        return new_status

    def count_symbol(self, symbol):
        return sum(seat_content == symbol for seat_content in self.layout.values())

    def find_seen_neighbours(self, cell):
        directions = [(i, j) for i in (-1, 0, 1) for j in (-1, 0, 1)]
        directions.remove((0, 0))
        seen_cells = set()

        for direction in directions:
            current_cell = cell
            found_seat = False
            while not found_seat:
                current_cell = (current_cell[0] + direction[0], current_cell[1] + direction[1])
                if not (0 <= current_cell[0] <= self.size[0] and 0 <= current_cell[1] <= self.size[1]):
                    break
                elif self.layout[current_cell] in (EMPTY, OCCUPIED):
                    seen_cells.add(current_cell)
                    found_seat = True
        return seen_cells


part = 2

layout = SeatState.parse_plan(seat_layout, prob=part)
# xx= layout.find_seen_neighbours((0,2))
same_layout = False

while not same_layout:
    new_layout = layout.transition_layout()
    if new_layout == layout:
        same_layout = True
    else:
        layout = new_layout
    print(new_layout.count_symbol(OCCUPIED))

print(f'Solution to part {part} is {layout.count_symbol(OCCUPIED)}')
