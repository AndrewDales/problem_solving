from dataclasses import dataclass, field
from collections import OrderedDict
from copy import deepcopy
import re

NUMBER_MINUTES = 30


@dataclass
class Valve:
    name: str
    open: bool = False
    release_rate: int = 0
    children: tuple[str, ...] = field(default_factory=list)

    def open_valve(self):
        self.open = True


with open("aoc_2022_16_test.txt") as file:
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

# unopened_valves = {valve_name for valve_name, c_valve in valve_dict.items() if c_valve.release_rate > 0}
unopened_valves = {valve_name for valve_name, c_valve in valve_dict.items()}


@dataclass
class ValvePath:
    round_number: int = 0
    visited: list[Valve, ...] = field(default_factory=list)
    unopened: set[str, ...] = field(default_factory=set)
    release_per_round: int = 0
    release_total: int = 0

    @property
    def current_valve(self):
        return self.visited[-1]

    @property
    def min_value(self):
        return self.release_per_round * (NUMBER_MINUTES - self.round_number) + self.release_total

    def max_value(self, v_dict=valve_dict):
        max_value = self.release_per_round * (NUMBER_MINUTES - self.round_number) + self.release_total
        rounds_left = NUMBER_MINUTES - self.round_number
        for f_valve in v_dict.values():
            rounds_left -= 2
            if rounds_left <= 0:
                break
            if f_valve.name in self.unopened:
                max_value += rounds_left * f_valve.release_rate
        if not self.current_valve.open:
            new_value = self.open_current_valve()
            max_value = max(max_value, new_value.max_value(v_dict))
        return max_value

    def increment_round(self):
        self.round_number += 1
        self.release_total += self.release_per_round

    def add_valve(self, new_valve: Valve):
        new_path = ValvePath(self.round_number,
                             deepcopy(self.visited),
                             self.unopened,
                             self.release_per_round,
                             self.release_total)
        if new_valve.name not in self.unopened:
            new_valve.open = True

        new_path.increment_round()
        new_path.visited.append(new_valve)
        return new_path

    def open_current_valve(self):
        if self.current_valve.open:
            raise TypeError("Current valve is already open")
        unopened = self.unopened - {self.current_valve.name}
        new_path = ValvePath(self.round_number,
                             deepcopy(self.visited),
                             unopened,
                             self.release_per_round,
                             self.release_total)
        new_path.increment_round()
        new_path.current_valve.open_valve()
        new_path.release_per_round += new_path.current_valve.release_rate
        return new_path

    def visit_children(self, v_dict, overall_min=0):
        # If current valve is unopened take the parent node out of the children
        children_to_visit = list(self.current_valve.children)
        if not self.current_valve.open and len(self.visited) > 1:
            children_to_visit.remove(self.visited[-2].name)

        child_paths = [self.add_valve(v_dict[child]) for child in children_to_visit]
        child_paths = [child for child in child_paths if child.max_value() > overall_min]

        if not self.current_valve.open and self.current_valve.release_rate > 0:
            child_paths.append(self.open_current_valve())
        return child_paths


base_path = ValvePath(visited=[valve_dict["AA"]], unopened=unopened_valves)



# path_1 = base_path.add_valve(valve_dict["DD"])
# path_2 = path_1.open_current_valve()
# path_3 = path_2.add_valve(valve_dict["CC"])
# path_4 = path_3.add_valve(valve_dict["DD"])
# path_5 = path_4.open_current_valve()
#
# path_4.max_value(valve_dict)
# # new_paths = path_1.visit_children(valve_dict)
# child_paths = base_path.visit_children(valve_dict)
# path_list = [base_path]
# global_min = 0
#
# for current_round in range(1, NUMBER_MINUTES):
#     new_path_list = []
#     for path in path_list:
#         new_path_list += path.visit_children(valve_dict, overall_min=global_min)
#     global_min = max(pth.min_value for pth in new_path_list)
#     print(current_round, global_min, len(new_path_list))
#     path_list = new_path_list
