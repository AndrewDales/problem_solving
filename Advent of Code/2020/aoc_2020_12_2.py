from dataclasses import dataclass
from aoc_2020_12 import MOVES

with open("aoc_2020_12.txt") as file:
    actions = [(line[0], int(line[1:])) for line in file]


@dataclass
class ShipState:
    position: tuple[int, int] = (0, 0)
    direction: str = "E"

    def resolve_action(self, action, number, way_point):
        if action in 'NEWS':
            way_point.move(action, number)
        if action == 'F':
            self.move(number, way_point.position)
        elif action in 'LR':
            way_point.rotate(action, number)

    def move(self, distance, wp_position):
        self.position = (self.position[0] + distance * wp_position[0], self.position[1] + distance * wp_position[1])


@dataclass
class WayPoint:
    position: tuple[int, int] = (0, 0)

    def move(self, action, distance):
        direction = MOVES[action]
        self.position = (self.position[0] + distance * direction[0], self.position[1] + distance * direction[1])

    def rotate(self, action, turn_angle):
        if action == 'R':
            turn_angle = 360 - turn_angle
        if turn_angle == 90:
            self.position = (self.position[1], -self.position[0])
        elif turn_angle == 180:
            self.position = (-self.position[0], -self.position[1])
        if turn_angle == 270:
            self.position = (-self.position[1], self.position[0])


my_ship = ShipState()
my_waypoint = WayPoint((1, 10))

for ship_action in actions:
    my_ship.resolve_action(*ship_action, my_waypoint)

print(f'Solution to part 2 is {abs(my_ship.position[0]) + abs(my_ship.position[1]) }')
