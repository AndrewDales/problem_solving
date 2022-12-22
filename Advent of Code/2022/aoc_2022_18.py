from collections import deque
from dataclasses import dataclass, field
from typing import AbstractSet

with open("aoc_2022_18.txt") as file:
    file_contents = set(tuple(int(el) for el in line.strip().split(",")) for line in file)

NEIGHBOUR_POS = {(0, 0, 1), (0, 1, 0), (1, 0, 0), (0, 0, -1), (0, -1, 0), (-1, 0, 0)}


def cube_neighbours(cube: tuple[int, int, int]) -> set[tuple[int, int, int]]:
    return set((cube[0] + pos[0],
                cube[1] + pos[1],
                cube[2] + pos[2])
               for pos in NEIGHBOUR_POS)


@dataclass
class LavaSystem:
    lava_cubes: AbstractSet[tuple[int, int, int] | None] = field(default_factory=set)
    exterior_cubes: AbstractSet[tuple[int, int, int] | None] = field(default_factory=set)
    interior_cubes: AbstractSet[tuple[int, int, int] | None] = field(default_factory=set)

    def __post_init__(self):
        self.min_coords = tuple(min(pos[i] for pos in self.lava_cubes) for i in range(3))
        self.max_coords = tuple(max(pos[i] for pos in self.lava_cubes) for i in range(3))
        self.possible_coords = set((i, j, k)
                                   for i in range(self.min_coords[0], self.max_coords[0] + 1)
                                   for j in range(self.min_coords[1], self.max_coords[1] + 1)
                                   for k in range(self.min_coords[2], self.max_coords[2] + 1)
                                   )

    @property
    def known_cubes(self):
        return self.lava_cubes | self.exterior_cubes | self.interior_cubes

    @property
    def unknown_cubes(self):
        return self.possible_coords - self.known_cubes

    def is_external(self, cube):
        return self.is_outside(cube) or (cube in self.exterior_cubes)

    def is_outside(self, cube):
        return not all(self.min_coords[i] <= cube[i] <= self.max_coords[i] for i in range(3))

    def find_connected_group(self, cube):
        # current_cube = cube
        visited = set()
        cube_queue = deque()
        cube_queue.append(cube)
        external = False

        while cube_queue:
            current_cube = cube_queue.popleft()
            if current_cube in visited or current_cube in self.known_cubes:
                continue
            neighbours = cube_neighbours(current_cube)
            if not external and any(self.is_external(ngh) for ngh in neighbours):
                external = True
            valid_neighbours = [ngh for ngh in neighbours if
                                (not self.is_outside(ngh) and
                                 ngh not in self.known_cubes and
                                 ngh not in visited)]
            cube_queue.extend(valid_neighbours)
            visited.add(current_cube)
        return visited, external

    def classify_cubes(self):
        while self.unknown_cubes:
            new_cube = self.unknown_cubes.pop()
            cube_group, ext = self.find_connected_group(new_cube)
            if ext:
                self.exterior_cubes |= cube_group
            else:
                self.interior_cubes |= cube_group

    def count_sides(self, excluded_cells):
        return sum(sum((ngh not in excluded_cells) for ngh in cube_neighbours(cube)) for cube in self.lava_cubes)


# noinspection PyTypeChecker
lava_system = LavaSystem(lava_cubes=file_contents)
print(f'Solution to Day 18 part 1 is {lava_system.count_sides(lava_system.lava_cubes)}')

lava_system.classify_cubes()
print(f'Solution to Day 18 part 1 is {lava_system.count_sides(lava_system.lava_cubes | lava_system.interior_cubes)}')
