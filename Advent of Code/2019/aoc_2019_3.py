with open("data/aoc_input_2019_3.txt", "r") as file:
    wires = [line.strip().split(',') for line in file]


class Wire:
    directions = {'R': (1, 0),
                  'U': (0, 1),
                  'L': (-1, 0),
                  'D': (0,-1),
                  }

    def __init__(self):
        self.start = (0, 0)
        self.current = (0, 0)
        self.wires = set()

    def move(self, direction):
        move_vec = self.directions[direction]
        new_coord = (self.current[0] + move_vec[0], self.current[1] + move_vec[1])
        self.wires.add(new_coord)
        self.current = new_coord

    def move_vector(self, move_command):
        direction = move_command[0]
        distance = int(move_command[1:])
        for _ in range(distance):
            self.move(direction)

    def move_sequence(self, move_sequence):
        for cmd in move_sequence:
            self.move_vector(cmd)

wire_set = []

for command_list in wires:
    wire_obj = Wire()
    wire_obj.move_sequence(command_list)
    wire_set.append(wire_obj)

crosses = wire_set[0].wires & wire_set[1].wires

closest_cross = min(abs(cross[0]) + abs(cross[1]) for cross in crosses)
print(closest_cross)
