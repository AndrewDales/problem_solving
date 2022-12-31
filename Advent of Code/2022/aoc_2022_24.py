from functools import lru_cache
from typing import FrozenSet
from math import lcm
import heapq as hq


with open("aoc_2022_24_test.txt") as file:
    file_lines = [line.strip() for line in file]

WALLS = frozenset({(i, j) for i, line in enumerate(file_lines) for j, mk in enumerate(line) if mk == '#'})
BLIZZARDS = frozenset({((i, j), mk) for i, line in enumerate(file_lines) for j, mk in enumerate(line) if mk in '<>^v'})
BLIZZARD_LOCS = frozenset(bz[0] for bz in BLIZZARDS)

ENTRY_POINT = (0, file_lines[0].index("."))
EXIT_POINT = (len(file_lines) - 1, file_lines[-1].index('.'))

HEIGHT = max(pos[0] for pos in WALLS) + 1
WIDTH = max(pos[1] for pos in WALLS) + 1

BLIZZARD_LCM = lcm(HEIGHT - 2, WIDTH - 2)


def move_blizzard(blizzard):
    blizzard_loc = blizzard[0]
    blizzard_symbol = blizzard[1]
    new_loc = None

    if blizzard_symbol == "^":
        new_loc = (blizzard_loc[0] - 2) % (HEIGHT - 2) + 1, blizzard_loc[1]
    elif blizzard_symbol == "v":
        new_loc = blizzard_loc[0] % (HEIGHT - 2) + 1, blizzard_loc[1]
    elif blizzard_symbol == ">":
        new_loc = blizzard_loc[0], blizzard_loc[1] % (WIDTH - 2) + 1
    elif blizzard_symbol == "<":
        new_loc = blizzard_loc[0], (blizzard_loc[1] - 2) % (WIDTH - 2) + 1
    return new_loc, blizzard_symbol


@lru_cache(maxsize=BLIZZARD_LCM)
def move_all_blizzards(num_moves: int):
    if num_moves == 0:
        return BLIZZARDS, BLIZZARD_LOCS
    else:
        blizzards, _ = move_all_blizzards(num_moves - 1)
        new_blizzards = frozenset({move_blizzard(bz) for bz in blizzards})
        new_locs = frozenset(bz[0] for bz in blizzards)
        return new_blizzards, new_locs


class Valley:
    def __init__(self,
                 current_position: tuple[int, int] = ENTRY_POINT,
                 rounds: int = 0,
                 exit_point: tuple[int, int] = EXIT_POINT,
                 parent=None,
                 ):
        self.current_position = current_position
        self.rounds = rounds
        self.parent = parent
        self.exit_point = exit_point
        self._walls = WALLS
        self.distance = (abs(self.current_position[0] - self.exit_point[0])
                         + abs(self.current_position[1] - self.exit_point[1]))
        self.score = self.rounds + 1 * self.distance

    def __hash__(self):
        return hash((self.current_position, self.rounds))

    def __eq__(self, other):
        return self.current_position == other.current_position and self.rounds == other.rounds

    def __gt__(self, other):
        return self.score > other.score

    def get_neighbours(self):
        directions = ((1, 0), (0, 1), (-1, 0), (0, -1))
        neighbours = []
        for dct in directions:
            new_pos = self.current_position[0] + dct[0], self.current_position[1] + dct[1]
            if (new_pos not in self._walls and
                    0 <= new_pos[0] <= HEIGHT and
                    0 <= new_pos[1] <= WIDTH):
                neighbours.append(new_pos)
        return neighbours

    def branch_valley(self):
        new_blizzards, new_blizzard_locs = move_all_blizzards((self.rounds + 1) % BLIZZARD_LCM)
        neighbours = self.get_neighbours()
        neighbours.append(self.current_position)
        return [Valley(ngh, self.rounds + 1, exit_point=self.exit_point, parent=self) for ngh in neighbours
                if ngh not in new_blizzard_locs]

    def show_grid(self):
        blizzards, blizzard_locs = move_all_blizzards(self.rounds % BLIZZARD_LCM)
        for row in range(HEIGHT):
            for col in range(WIDTH):
                if (row, col) in self._walls:
                    print('#', end='')
                elif (row, col) == self.current_position:
                    print('E', end='')
                elif (row, col) == self.exit_point:
                    print('X', end='')
                elif (row, col) in blizzard_locs:
                    blizzards_in_loc = [bz for bz in blizzards if bz[0] == (row, col)]
                    if len(blizzards_in_loc) == 1:
                        print(blizzards_in_loc[0][1], end='')
                    else:
                        print(str(len(blizzards_in_loc)), end='')
                else:
                    print('.', end='')
            print()
        print()


def find_path(current_round=0, entry=ENTRY_POINT, exit=EXIT_POINT):

    current_valley = Valley(current_position=entry,
                            rounds=current_round,
                            exit_point=exit)
    min_dist = current_valley.distance

    i = 0
    visited = set()
    pq = []
    hq.heappush(pq, current_valley)
    reached_exit = False

    while not reached_exit:
        current_valley = hq.heappop(pq)
        if current_valley.distance < min_dist:
            min_dist = current_valley.distance
            print(current_valley.rounds, current_valley.distance)
        if current_valley in visited:
            continue
        visited.add(current_valley)
        if current_valley.current_position == exit:
            reached_exit = True
        else:
            neighbours = current_valley.branch_valley()
            for ngh in neighbours:
                if ngh not in visited:
                    hq.heappush(pq, ngh)
        # i += 1
        # if i >= 1_000:
        #     break

    return current_valley


trip_there = find_path()
# print("Arrived at exit 1st time")
# trip_back = find_path(current_round=trip_there.rounds, entry=trip_there.current_position, exit=ENTRY_POINT)
# print("Arrived back at start")
# trip_final = find_path(current_round=trip_back.rounds, entry=trip_back.current_position, exit=EXIT_POINT)
# print("Final arrival at exit\n")
#
print(f"Time for first trip = {trip_there.rounds}")
# print(f"Time for total trip = {trip_final.rounds}")
