from itertools import pairwise

with open("aoc_2022_14.txt") as file:
    file_contents = file.readlines()


def find_points_path(p_1, p_2):
    p_start, p_end = sorted((p_1, p_2))
    return set((i, j) for i in range(p_start[0], p_end[0] + 1) for j in range(p_start[1], p_end[1] + 1))


class Cave:
    @classmethod
    def parse_file(cls, p_file_contents):
        rocks = set()
        for line in p_file_contents:
            path_ends = [tuple(int(val) for val in pair.split(",")) for pair in line.strip().split('->')]
            for start_point, end_point in pairwise(path_ends):
                rocks.update(find_points_path(start_point, end_point))
        return rocks

    def __init__(self, rock_locations: set[tuple[int, int]]):
        self.rock_locations = rock_locations
        self.sand_locations = set()
        self.bottom_row = max(j for _, j in self.rock_locations)
        self.initial_sand_pos = (500, 0)
        self.blocks = self.rock_locations | self.sand_locations

    def place_sand(self):
        sand_loc = self.initial_sand_pos
        sand_falling = True

        while sand_falling:
            if sand_loc[1] >= self.bottom_row:
                break

            # Try below
            if (new_loc := (sand_loc[0], sand_loc[1] + 1)) not in self.blocks:
                sand_loc = new_loc
            # Try below left
            elif (new_loc := (sand_loc[0] - 1, sand_loc[1] + 1)) not in self.blocks:
                sand_loc = new_loc
            # Try below right
            elif (new_loc := (sand_loc[0] + 1, sand_loc[1] + 1)) not in self.blocks:
                sand_loc = new_loc
            else:
                sand_falling = False

        # Runs if while loop end (sand_falling = False)
        else:
            self.sand_locations.add(sand_loc)
            self.blocks.add(sand_loc)

        return sand_loc

    def pour_sand(self):
        sand_stopped = False
        while not sand_stopped:
            sand_location = self.place_sand()
            # if len(self.sand_locations) % 1000 == 0:
            #     print(len(self.sand_locations))
            if (sand_location[1] >= self.bottom_row) or (sand_location == self.initial_sand_pos):
                sand_stopped = True


class CaveFloor(Cave):
    def __init__(self, rock_locations: set[tuple[int, int]]):
        super().__init__(rock_locations)
        self.bottom_row = max(j for _, j in self.rock_locations) + 2
        self.rock_locations.update(bottom_blocks := find_points_path(
            (500 - self.bottom_row, self.bottom_row), (500 + self.bottom_row, self.bottom_row)))
        self.blocks.update(bottom_blocks)


my_rocks = Cave.parse_file(file_contents)
my_cave = Cave(my_rocks)
my_cave.pour_sand()
print(f'Units of sand in cave problem 1 = {len(my_cave.sand_locations)}')

my_second_cave = CaveFloor(my_rocks)
my_second_cave.pour_sand()
print(f'Units of sand in cave problem 2 = {len(my_second_cave.sand_locations)}')