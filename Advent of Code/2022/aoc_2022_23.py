from dataclasses import dataclass, field
from typing import Callable

with open("aoc_2022_23.txt") as file:
    file_lines = [line.strip() for line in file]

elves_initial = {(i, j) for i, line in enumerate(file_lines) for j, mk in enumerate(line) if mk == '#'}

MAX_ROUNDS = 100_000


@dataclass
class ElfGrid:
    elves: set[tuple[int, int]] = field(default_factory=set)
    round: int = 0
    checking_funcs: list[Callable, ...] = field(default_factory=list)

    def __post_init__(self):
        self.checking_funcs = [self.check_north, self.check_south, self.check_west, self.check_east]

    @property
    def height_range(self):
        return min(pos[0] for pos in self.elves), max(pos[0] for pos in self.elves)

    @property
    def width_range(self):
        return min(pos[1] for pos in self.elves), max(pos[1] for pos in self.elves)

    @staticmethod
    def get_neighbours(elf_pos):
        return {'ne': (elf_pos[0] - 1, elf_pos[1] + 1),
                'n': (elf_pos[0] - 1, elf_pos[1]),
                'nw': (elf_pos[0] - 1, elf_pos[1] - 1),
                'w': (elf_pos[0], elf_pos[1] - 1),
                'sw': (elf_pos[0] + 1, elf_pos[1] - 1),
                's': (elf_pos[0] + 1, elf_pos[1]),
                'se': (elf_pos[0] + 1, elf_pos[1] + 1),
                'e': (elf_pos[0], elf_pos[1] + 1),
                # 'current': elf_pos
                }

    def check_north(self, elf_neighbours):
        if not {elf_neighbours['ne'], elf_neighbours['nw'], elf_neighbours['n']} & self.elves:
            return elf_neighbours['n']

    def check_south(self, elf_neighbours):
        if not {elf_neighbours['se'], elf_neighbours['sw'], elf_neighbours['s']} & self.elves:
            return elf_neighbours['s']

    def check_west(self, elf_neighbours):
        if not {elf_neighbours['w'], elf_neighbours['sw'], elf_neighbours['nw']} & self.elves:
            return elf_neighbours['w']

    def check_east(self, elf_neighbours):
        if not {elf_neighbours['e'], elf_neighbours['se'], elf_neighbours['ne']} & self.elves:
            return elf_neighbours['e']

    def rotate_functions(self):
        self.checking_funcs = self.checking_funcs[1:] + self.checking_funcs[:1]

    def proposed_position(self, elf: tuple[int, int]) -> tuple[int, int]:
        elf_neighbours = self.get_neighbours(elf)
        # Check no neighbours i.e. no move
        if not (set(elf_neighbours.values()) & elf_grid.elves):
            proposed_position = elf
        else:
            for f in self.checking_funcs:
                proposed_position = f(elf_neighbours)
                if proposed_position:
                    break
            else:
                proposed_position = elf
        return proposed_position

    def proposed_moves(self) -> dict[tuple[int, int]: tuple[int, int]]:
        moves = {elf: self.proposed_position(elf) for elf in self.elves}
        return moves

    def resolve_moves(self) -> set[tuple[int, int]]:
        final_pos = []
        proposed_moves = self.proposed_moves()
        prop_ends = tuple(proposed_moves.values())
        for orig_pos, prop_pos in proposed_moves.items():
            if prop_ends.count(prop_pos) == 1:
                final_pos.append(prop_pos)
            else:
                final_pos.append(orig_pos)
        return set(final_pos)

    def resolve_round(self):
        self.round += 1
        new_pos = self.resolve_moves()
        # Check if finished - no elves move
        if new_pos == self.elves:
            return True
        self.elves = new_pos
        self.rotate_functions()
        return False

    def show_grid(self):
        for row in range(self.height_range[0], self.height_range[1] + 1):
            for col in range(self.width_range[0], self.width_range[1] + 1):
                if (row, col) in self.elves:
                    print('#', end='')
                else:
                    print('.', end='')
            print()
        print()

    def run_sequence(self, num_rounds=MAX_ROUNDS):
        print("== Initial State (round {self.round}) ==")
        self.show_grid()

        for _ in range(1, num_rounds + 1):
            if self.resolve_round():
                break
            print(f'== End of Round {self.round} ==')
            self.show_grid()

        else:
            print(f'Elves still moving after {self.round} rounds')

        print(f"== Final State (round {self.round}) ==")
        self.show_grid()

    def find_empty_ground(self):
        rectangle_area = (self.height_range[1] - self.height_range[0] + 1) * \
                         (self.width_range[1] - self.width_range[0] + 1)
        return rectangle_area - len(self.elves)


elf_grid = ElfGrid(elves=elves_initial)
elf_grid.run_sequence(10)

print(f'Solution to Day 23, Problem 1 is {elf_grid.find_empty_ground()}')

elf_grid.run_sequence()

print(f'Solution to Day 23, Problem 2 is {elf_grid.round}')
