from dataclasses import dataclass, field
from collections import OrderedDict
from copy import deepcopy
import re
import heapq

NUMBER_MINUTES = 30


@dataclass
class Valve:
    name: str
    open: bool = False
    release_rate: int = 0
    children: tuple[str, ...] = field(default_factory=list)

    # def open_valve(self):
    #     self.open = True


@dataclass(order=True)
class ValvePath:
    current_valve_name: str
    opened: set[str, ...] = field(default_factory=set)
    unopened: set[str, ...] = field(default_factory=set)
    round_number: int = field(default=0, compare=False)
    release_per_round: int = field(default=0, compare=False)
    release_total: int = field(default=0, compare=False)
    all_valves: dict[str: Valve, ...] = field(default_factory=dict, compare=False)

    @property
    def min_value(self):
        return self.release_per_round * (NUMBER_MINUTES - self.round_number) + self.release_total

    @property
    def max_value(self):
        max_value = self.min_value
        rounds_left = NUMBER_MINUTES - self.round_number
        for f_valve in self.all_valves.values():
            rounds_left -= 2
            if rounds_left <= 0:
                break
            if f_valve.name in self.unopened:
                max_value += rounds_left * f_valve.release_rate
        if self.current_valve_name not in self.opened:
            new_path = self.open_current_valve()
            max_value = max(max_value, new_path.max_value)
        return max_value

    @property
    def current_valve(self):
        return self.all_valves[self.current_valve_name]

    def increment_round(self):
        self.round_number += 1
        self.release_total += self.release_per_round

    def open_current_valve(self):
        if self.current_valve_name in self.opened:
            raise TypeError("Current valve is already open")
        new_path = deepcopy(self)
        new_path.opened.add(self.current_valve_name)
        new_path.unopened.remove(self.current_valve_name)
        new_path.increment_round()
        new_path.release_per_round += self.current_valve.release_rate
        return new_path

    def add_valve(self, new_valve):
        new_path = deepcopy(self)
        new_path.current_valve_name = new_valve
        new_path.increment_round()
        return new_path

    def find_children(self):
        children = [self.add_valve(child) for child in self.current_valve.children]
        if self.current_valve_name not in self.opened and self.current_valve.release_rate > 0:
            children.append(self.open_current_valve())
        return children

    def state_tuple(self):
        return (self.current_valve_name,
                frozenset(self.opened),
                frozenset(self.unopened),
                )


with open("aoc_2022_16.txt") as file:
    file_contents = file.read()

valve_data = re.findall(r'Valve\s([A-Z]{2}).*rate=(\d+).*valves? ([A-Z].*[A-Z])', file_contents)

valve_list = []
for line in valve_data:
    valve = line[0]
    rate = int(line[1])
    children = tuple(v.strip() for v in line[2].split(","))
    valve_list.append((valve, Valve(valve, open=False, release_rate=rate, children=children)))

valve_list.sort(key=lambda x: x[1].release_rate, reverse=True)
valve_dict = OrderedDict(valve_list)

base_path = ValvePath(current_valve_name="AA",
                      unopened=set(valve_dict.keys()),
                      all_valves=valve_dict)

# path_1 = base_path.add_valve("DD")
# path_2 = path_1.open_current_valve()
# path_3 = path_2.add_valve("CC")
# path_4 = path_3.add_valve("DD")
# path_5 = path_4.open_current_valve()

# path = base_path.add_valve("DD")
# path = base_path.open_current_valve()
# path = base_path.add_valve("CC")


visited = set()
pq = []

heapq.heappush(pq, (-base_path.max_value, -base_path.min_value, base_path))
global_max = base_path.max_value
global_min = base_path.min_value

while pq:
    current_max, current_min, current_path = heapq.heappop(pq)
    current_max *= -1
    current_min *= -1

    global_max = min(global_max, current_max)
    global_min = max(global_min, current_min)
    print(global_max, global_min)
    if current_min >= current_max:
        break

    visited.add(current_path.state_tuple())

    for child in current_path.find_children():
        if child.state_tuple() in visited or child.max_value <= global_min:
        # if child.max_value <= global_min:
            continue
        else:
            heapq.heappush(pq, (-child.max_value, -child.min_value, child))
