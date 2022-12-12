with open("aoc_2022_9.txt") as file:
    lines = [line.strip().split() for line in file]
    move_sequence = [(line[0], int(line[1])) for line in lines]


def nearer(x: int) -> int:
    if abs(x) < 1:
        x_new = x
    elif x > 0:
        x_new = x - 1
    else:
        x_new = x + 1
    return x_new


def add_vector(v1, v2):
    return v1[0] + v2[0], v1[1] + v2[1]


def sub_vector(v1, v2):
    return v1[0] - v2[0], v1[1] - v2[1]


class RopePos:
    no_move = tuple((i, j) for i in range(-1, 2) for j in range(-1, 2))
    two_away = tuple((i, j) for i in range(-2, 3) for j in range(-2, 3)
                     if (abs(i) == 2 or abs(j) == 2))
    tail_from_head = {mv: mv for mv in no_move}
    tail_from_head.update({mv: (nearer(mv[0]), nearer(mv[1])) for mv in two_away})
    directions = {"U": (1, 0), "R": (0, 1), "D": (-1, 0), "L": (0, -1)}

    def __init__(self, num_sections):
        self.num_sections = num_sections
        self.sections_pos = [(0,0)] * num_sections
        self.tail_positions = {(0, 0)}

    def move_tail_head(self, direction: str, distance: int):
        dir_vector = self.directions[direction]
        for _ in range(distance):
            self.sections_pos[0] = add_vector(self.sections_pos[0], dir_vector)
            prev_section_pos = self.sections_pos[0]
            for i, sect_pos in enumerate(self.sections_pos[1:], 1):
                cur_pos_to_prev_section = sub_vector(sect_pos, prev_section_pos)
                new_pos_to_prev_section= self.tail_from_head[cur_pos_to_prev_section]
                self.sections_pos[i] = add_vector(prev_section_pos, new_pos_to_prev_section)
                prev_section_pos = self.sections_pos[i]

            self.tail_positions.add(self.sections_pos[-1])

        # print(f'{root_dir.sections_pos[0]=} {root_dir.sections_pos[1]=}')

    def move_from_sequence(self, sequence):
        for mv_dir, mv_dis in sequence:
            self.move_tail_head(mv_dir, mv_dis)


rop = RopePos(2)
rop.move_from_sequence(move_sequence)

print(f'Solution to Problem 1 is {len(rop.tail_positions)}')

rop_multi = RopePos(10)
rop_multi.move_from_sequence(move_sequence)

print(f'Solution to Problem 2 is {len(rop_multi.tail_positions)}')
