import math


def is_square(x: int):
    return x == x > 0 and math.floor(math.sqrt(x)) ** 2


def cartesian_distance(x_1, y_1, x_2, y_2):
    return (x_2 - x_1) ** 2 + (y_2 - y_1) ** 2


def is_opq_right_angled(x_1, y_1, x_2, y_2):
    return (cartesian_distance(x_1, y_1, x_2, y_2) +
            cartesian_distance(x_1, y_1, 0, 0) ==
            cartesian_distance(0, 0, x_2, y_2) and
            (x_1, y_1) != (x_2, y_2) and
            (x_1, y_1) != (0, 0))


MAX_COORD = 50

# The number of triangles where OPQ is right-angled
number_OPQ_right_angled = sum(is_opq_right_angled(a, b, c, d)
                              for a in range(MAX_COORD + 1)
                              for b in range(MAX_COORD + 1)
                              for c in range(MAX_COORD + 1)
                              for d in range(MAX_COORD + 1)
                              )

# Number of triangles where POQ is right-angled
number_POQ_right = MAX_COORD ** 2

print(f'Solution to Project Euler 91 is {number_POQ_right + number_OPQ_right_angled}')
