from dataclasses import dataclass, field
from collections import OrderedDict, deque
from copy import deepcopy
import re
import heapq as hq

NUMBER_MINUTES = 30

with open("aoc_2022_16.txt") as file:
    file_contents = file.read()

valve_data = re.findall(r'Valve\s([A-Z]{2}).*rate=(\d+).*valves? ([A-Z].*[A-Z])', file_contents)


class Valve:
    def __init__(self, name, release_rate, children):
        self.name: str = name
        self.release_rate: int = release_rate
        self.children: tuple[str, ...] = children

    def __gt__(self, other):
        return self.release_rate > other.release_rate

    def __eq__(self, other):
        return self.name == other.name



def find_distances(valve: str):
    valve_dist = dict()
    valve_queue = [(0, valve)]

    while valve_queue:
        current_dist, current_valve = hq.heappop(valve_queue)
        if current_valve not in valve_dist.keys():
            valve_dist[current_valve] = current_dist
        else:
            continue
        neighbours = [(current_dist + 1, VALVE_DICT[child].name)
                      for child in VALVE_DICT[current_valve].children
                      if child not in valve_dist.keys()
                      ]
        for ngh in neighbours:
            hq.heappush(valve_queue, ngh)
    return valve_dist


valve_list = []
for line in valve_data:
    valve = line[0]
    rate = int(line[1])
    children = tuple(v.strip() for v in line[2].split(","))
    valve_list.append((valve, Valve(valve, release_rate=rate, children=children)))

valve_list.sort(key=lambda x: x[1].release_rate, reverse=True)
VALVE_DICT = OrderedDict(valve_list)
VALVE_NAMES = frozenset(VALVE_DICT.keys())
VALVE_POSITIVE = [valve.name for valve in VALVE_DICT.values() if valve.release_rate > 0]

VALVE_DISTANCES = {valve: find_distances(valve) for valve in VALVE_NAMES}


class ValvePath:
    def __init__(self, my_current_valve, opened, round_number=0, release_total=0,
                 elephant_current_valve=None):
        self.current_valve_name: str = my_current_valve
        self.elephant_current_valve: str | None = elephant_current_valve
        self.opened: frozenset[str, ...] = opened
        self.round_number: int = round_number
        self.release_total: int = release_total
        self.release_per_round: int = sum(VALVE_DICT[val].release_rate for val in self.opened)
        self.unopened = frozenset(VALVE_NAMES - set(self.opened))
        self.min_value = self.release_per_round * (NUMBER_MINUTES - self.round_number) + self.release_total
        self.value = self.find_value()

    def find_value(self):
        max_value = self.min_value
        rounds_left = NUMBER_MINUTES - self.round_number
        max_value += sum((VALVE_DICT[valve].release_rate *
                          max(rounds_left - VALVE_DISTANCES[self.current_valve_name][valve] - 1,0))
                         for valve in self.unopened)
        return max_value

    def find_min_value(self):
        rounds_left = NUMBER_MINUTES - self.round_number
        min_value = self.release_per_round * (NUMBER_MINUTES - self.round_number) + self.release_total
        positive_unopened = [valve in VALVE_POSITIVE if valve in self.unopened]
        while rounds_left > 0 and positive_unopened:




    @property
    def current_valve(self):
        return VALVE_DICT[self.current_valve_name]

    # def increment_round(self):
    #     self.round_number += 1
    #     self.release_total += self.release_per_round

    def open_current_valve(self):
        if self.current_valve_name in self.opened:
            raise TypeError("Current valve is already open")
        open_set = set(self.opened) | {self.current_valve_name}
        opened = frozenset(open_set)
        new_path = ValvePath(self.current_valve_name,
                             opened,
                             self.round_number + 1,
                             self.release_total + self.release_per_round)
        return new_path

    def add_valve(self, new_valve):
        new_path = ValvePath(new_valve, self.opened, self.round_number + 1, self.release_total + self.release_per_round)
        return new_path

    def find_children(self):
        children = [self.add_valve(child) for child in self.current_valve.children]
        if self.current_valve_name not in self.opened and self.current_valve.release_rate > 0:
            children.append(self.open_current_valve())
        children.sort(reverse=True)
        return children

    # def state_tuple(self):
    #     return (self.current_valve_name,
    #             frozenset(self.opened),
    #             frozenset(self.unopened),
    #             )

    def __gt__(self, other):
        return (self.value, self.min_value) > (other.value, other.min_value)

    def __hash__(self):
        return hash((self.current_valve_name, self.elephant_current_valve, self.round_number, self.opened,
                     self.release_total))


base_path = ValvePath(my_current_valve="AA",
                      opened=frozenset({}),
                      )


current_paths = [base_path]

# for rounds in range(NUMBER_MINUTES):
#     new_paths = []
#     for path in current_paths:
#         new_paths += path.find_children()
#     new_paths = list(set(new_paths))
#     new_paths.sort(reverse=True)
#     current_paths = new_paths[:2000]
#
# print(f'Solution to Day 16, part 1 is {current_paths[0].release_total}')

# visited = set()
# pq = []
#
# hq.heappush(pq, (-base_path.value, -base_path.min_value, base_path))
# global_max = base_path.value
# global_min = base_path.min_value
#
# while pq:
#     current_max, current_min, current_path = hq.heappop(pq)
#     current_max *= -1
#     current_min *= -1
#
#     global_max = min(global_max, current_max)
#     global_min = max(global_min, current_min)
#     print(global_max, global_min)
#     if current_min >= current_max:
#         break
#
#     visited.add(current_path)
#
#     for child in current_path.find_children():
#         if child in visited or child.value <= global_min:
#         # if child.max_value <= global_min:
#             continue
#         else:
#             hq.heappush(pq, (-child.value, -child.min_value, child))
