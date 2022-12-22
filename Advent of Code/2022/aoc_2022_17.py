from dataclasses import dataclass, field
from itertools import cycle, pairwise

ROCKS = cycle((((0, 0), (1, 0), (2, 0), (3, 0)),
               ((1, 0), (0, 1), (1, 1), (2, 1), (1, 2)),
               ((0, 0), (1, 0), (2, 0), (2, 1), (2, 2)),
               ((0, 0), (0, 1), (0, 2), (0, 3)),
               ((0, 0), (1, 0), (0, 1), (1, 1)),
               ))

DIRECTIONS = {">": (1, 0),
              "<": (-1, 0),
              "d": (0, -1),
              }

NUM_ROCKS_1 = 2022
NUM_ROCKS_2 = 1_000_000_000_000


with open("aoc_2022_17.txt") as file:
    file_contents = file.read().strip()

# gas_commands = cycle(file_contents)

NUM_ROCKS_CYCLE = len(file_contents * 5)




@dataclass
class Rock:
    rock_coords: tuple[tuple[int, int], ...]
    position: list[int, int] = field(default_factory=lambda: [2, 3])

    @property
    def bottom(self) -> int:
        return self.position[1]

    @property
    def left(self) -> int:
        return self.position[0]

    @bottom.setter
    def bottom(self, value: int):
        self.position[1] = value

    @left.setter
    def left(self, value: int):
        self.position[0] = value

    @property
    def rock_positions(self) -> tuple[tuple[int, int], ...]:
        return tuple((pos[0] + self.left, pos[1] + self.bottom) for pos in self.rock_coords)

    @property
    def top(self):
        return max(pos[1] for pos in self.rock_positions)

    @property
    def right(self):
        return max(pos[0] for pos in self.rock_positions)

    def move(self, direction):
        direction_vector = DIRECTIONS[direction]
        new_position = [self.position[0] + direction_vector[0], self.position[1] + direction_vector[1]]
        new_rock = Rock(self.rock_coords, new_position)
        return new_rock


@dataclass
class Shaft:
    max_width: int = 6
    height: int = -1
    falling_rock: Rock | None = None
    settled_rocks: set[tuple[int, int], ...] = field(default_factory=set)

    def add_rock(self, rock: Rock):
        if self.falling_rock is not None:
            raise RuntimeError("Shaft already has a falling rock")
        rock.left = 2
        rock.bottom = self.height + 4
        self.falling_rock = rock

    def check_collision(self, rock: Rock) -> bool:
        return any(rock_pos in self.settled_rocks for rock_pos in rock.rock_positions)

    def horizontal_move(self, h_direction):
        new_rock = self.falling_rock.move(h_direction)
        # Check new_rock is not too far right, left, or hitting a settled rock
        if not (new_rock.right > self.max_width or
                new_rock.left < 0 or
                (new_rock.bottom <= self.height and self.check_collision(new_rock))):
            self.falling_rock = new_rock

    def down_move(self):
        new_rock = self.falling_rock.move("d")
        # Check a collision has taken place
        if new_rock.bottom < 0 or new_rock.bottom <= self.height and self.check_collision(new_rock):
            falling_rock_set = set(self.falling_rock.rock_positions)
            self.settled_rocks |= falling_rock_set
            self.height = max(max(pos[1] for pos in falling_rock_set), self.height)
            self.falling_rock = None
        else:
            self.falling_rock = new_rock

    def reduce(self):
        self.settled_rocks = {rock for rock in self.settled_rocks if rock[1] > self.height - 1000}

    def __str__(self):
        shaft_ascii = ""
        if self.falling_rock:
            draw_height = self.falling_rock.top
        else:
            draw_height = self.height
        for i in range(draw_height, -1, -1):
            line = "|"
            for j in range(0, self.max_width + 1):
                if self.falling_rock and (j, i) in self.falling_rock.rock_positions:
                    symbol = "@"
                elif (j, i) in self.settled_rocks:
                    symbol = "#"
                else:
                    symbol = "."
                line += symbol
            line += "|\n"
            shaft_ascii += line
        shaft_ascii += "+" + "-" * (self.max_width + 1) + "+"
        return shaft_ascii


def height_shaft(num_cycles):
    # my_shaft = Shaft()
    for i in range(1, num_cycles+1):
        my_shaft.add_rock(Rock(next(ROCKS)))

        while my_shaft.falling_rock:
            h_dir = next(gas_commands)
            my_shaft.horizontal_move(h_dir)
            my_shaft.down_move()
        if i % 50455 == 0:
            my_shaft.reduce()
            print(i, my_shaft.height + 1)
    return my_shaft.height + 1


# print(f'Height of tower in part one is {height_shaft(NUM_ROCKS_1, cycle(file_contents))}')
my_shaft = Shaft()
gas_commands = cycle(file_contents)

heights = [0]
height_change = []

# for i in range(1, 1000):
#     heights.append(height_shaft(NUM_ROCKS_CYCLE))
#     height_change.append(heights[-1] - heights[-2])
#     print(i, heights[-1], height_change[-1])
#     my_shaft.reduce()
    # if height_change[-3:] in [[height_change[i], height_change[i+1], height_change[i+2]] for i in range(len(height_change)-4)]:
    #     break

# height_full_cycle = height_shaft(NUM_ROCKS_CYCLE, cycle(file_contents))
# quot, rem = divmod(NUM_ROCKS_2, NUM_ROCKS_CYCLE)
# height_rem = height_shaft(rem, cycle(file_contents))
#
# print(f'Height of tower in part two is {quot * height_full_cycle + height_rem}')

# resid_height = height_shaft(NUM_ROCKS_CYCLE*4)
resid_height = height_shaft(31_749_540)

with open("aoc_2022_output_17.txt","w") as file:
    file.writelines(str(h)+"\n" for h in heights)

