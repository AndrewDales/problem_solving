import re
from dataclasses import dataclass, field
from typing import DefaultDict
from collections import defaultdict
from copy import deepcopy
from math import prod

with open("aoc_2022_19.txt") as file:
    file_contents = file.read()

blueprint_data = re.findall(r'ore robot.*?(\d+).*?clay robot.*?(\d+).*?obsidian robot.*?(\d+) ore.*?(\d+) clay.*?geode '
                            r'robot.*?(\d+) ore.*?(\d+) obsidian',
                            file_contents)
blueprint_data = [tuple(int(i) for i in lst) for lst in blueprint_data]

blueprint_costs = [{"ore_rob": (blue_print_tup[0], 0, 0, 0),
                    "clay_rob": (blue_print_tup[1], 0, 0, 0),
                    "obsidian_rob": (*blue_print_tup[2:4], 0, 0),
                    "geode_rob": (blue_print_tup[4], 0, blue_print_tup[5], 0),
                    }
                   for blue_print_tup in blueprint_data]

NUM_MINUTES = 32


@dataclass
class RobotState:
    blueprint: dict[str:tuple[int, int, int]]
    minute: int = 0
    robots: dict[str: int] = field(default_factory=lambda: {"ore_rob": 1,
                                                            "clay_rob": 0,
                                                            "obsidian_rob": 0,
                                                            "geode_rob": 0})
    materials: list[int, int, int, int] = field(default_factory=lambda: [0, 0, 0, 0])

    @property
    def time_remaining(self):
        return NUM_MINUTES - self.minute

    @property
    def value(self):
        value = self.materials[3]

        partial_robots = {"ore_rob": self.robots["ore_rob"] + 0.1 * self.materials[0] / self.blueprint["ore_rob"][0],
                          "clay_rob": self.robots["clay_rob"] + 0.1 * self.materials[0] / self.blueprint["clay_rob"][0],
                          "obsidian_rob": (self.robots["obsidian_rob"] + 0.5 * self.materials[1] /
                                           self.blueprint["obsidian_rob"][1]),
                          "geode_rob": (self.robots["geode_rob"] + 0.5 * self.materials[2] /
                                        self.blueprint["geode_rob"][2])}

        value += partial_robots["geode_rob"] * max(0, self.time_remaining - 1)
        value += (partial_robots["obsidian_rob"] * max(0, self.time_remaining - 2) ** 2 /
                  (2 * self.blueprint["geode_rob"][2]))
        value += (partial_robots["clay_rob"] * max(0, self.time_remaining - 3) ** 3 /
                  (6 * self.blueprint["obsidian_rob"][1] * self.blueprint["geode_rob"][2]))
        value += (partial_robots["ore_rob"] * max(0, self.time_remaining - 4) ** 4 /
                  (24 * self.blueprint["clay_rob"][0] * self.blueprint["obsidian_rob"][1]
                   * self.blueprint["geode_rob"][2]))
        return value

    def increment_minute(self, new_materials):
        self.materials = [self.materials[i] + new_materials[i] for i in range(4)]
        self.minute += 1

    def max_affordable(self, robot_type):
        return min(self.materials[i] // self.blueprint[robot_type][i] for i in range(3)
                   if self.blueprint[robot_type][i] > 0)

    def buy_robot(self, robot_type, number):
        cost = self.blueprint[robot_type]
        self.robots[robot_type] += number
        self.materials = [self.materials[i] - number * self.blueprint[robot_type][i] for i in range(4)]

    def branch_robots(self):
        new_materials_produced = list(self.robots.values())
        # No purchase rob
        rob = deepcopy(self)
        new_robot_states = [rob]

        # buy robots
        for robot_type in self.blueprint.keys():
            if rob.max_affordable(robot_type) >= 1:
                new_rob = deepcopy(rob)
                new_rob.buy_robot(robot_type, 1)
                new_robot_states.append(new_rob)

        # Old - assume that you can but as many as you like of any type of robot
        # for robot_type in self.blueprint.keys():
        #     new_type_robot_states = []
        #     for rob in new_robot_states:
        #         for i in range(1, rob.max_affordable(robot_type) + 1):
        #             new_type_robot = deepcopy(rob)
        #             new_type_robot.buy_robot(robot_type, i)
        #             new_type_robot_states.append(new_type_robot)
        #     new_robot_states += new_type_robot_states

        for rs in new_robot_states:
            rs.increment_minute(new_materials_produced)
        return new_robot_states

    def state_tuple(self):
        return (tuple(self.robots.values()),
                tuple(self.materials),
                self.minute)

    def __gt__(self, other):
        return self.value > other.value


def find_max_geodes(blue_print):
    current_states = [RobotState(blueprint=blue_print)]

    for i in range(NUM_MINUTES):
        new_states = []
        visited = set()
        for state in current_states:
            branched_states = state.branch_robots()
            for b_state in branched_states:
                if b_state.state_tuple() not in visited:
                    visited.add(b_state.state_tuple())
                    new_states.append(b_state)
        new_states.sort(reverse=True)
        current_states = deepcopy(new_states[:500])

    return max(cs.materials[3] for cs in current_states)


max_geodes = []
for blueprint in blueprint_costs[:3]:
    mg = find_max_geodes(blue_print=blueprint)
    print(mg)
    max_geodes.append(mg)

# print(f'Answer to Day 19 problem 1 = {sum(mg * i for i, mg in enumerate(max_geodes, 1))}')
print(f'Answer to Day 19 problem 2 = {prod(mg for  mg in max_geodes)}')



# test_state = RobotState(blueprint=blue_print, minute=7,
#                         robots={"ore_rob": 1,
#                                 "clay_rob": 3,
#                                 "obsidian_rob": 0,
#                                 "geode_rob": 0},
#                         materials=[2, 4, 0, 0])
#
# new_test_states = test_state.branch_robots()

# test_state = RobotState(blueprint=blue_print, minute=10,
#                         robots={"ore_rob": 1,
#                                 "clay_rob": 3,
#                                 "obsidian_rob": 0,
#                                 "geode_rob": 0},
#                         materials=[4, 15, 0, 0])
#
# new_test_states = test_state.branch_robots()
