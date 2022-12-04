from dataclasses import dataclass, field
from bidict import bidict

with open("aoc_2020_12.txt") as file:
    actions = [(line[0], int(line[1:])) for line in file]

MOVES = {'N': (1, 0),
         'E': (0, 1),
         'S': (-1, 0),
         'W': (0, -1),
         }
DIRECTIONS = bidict({0: 'E',
                     90: 'N',
                     180: 'W',
                     270: 'S',
                     })


@dataclass
class ShipState:
    position: tuple[int, int] = (0, 0)
    direction: str = "E"

    def resolve_action(self, action, number):
        if action in 'NEWSF':
            self.move(action, number)
        elif action in 'LR':
            self.rotate(action, number)

    def move(self, action, distance):
        if action == 'F':
            action = self.direction
        direction = MOVES[action]
        self.position = (self.position[0] + distance * direction[0], self.position[1] + distance * direction[1])

    def rotate(self, action, turn_angle):
        if action == 'R':
            turn_angle = -turn_angle
        current_angle = DIRECTIONS.inverse[self.direction]
        self.direction = DIRECTIONS[(current_angle + turn_angle) % 360]


my_ship = ShipState()

for ship_action in actions:
    my_ship.resolve_action(*ship_action)

print(f'Solution to part 1 is {abs(my_ship.position[0]) + abs(my_ship.position[1]) }')
