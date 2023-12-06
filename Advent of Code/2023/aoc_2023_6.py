from math import sqrt, floor, ceil, prod, isqrt

# times = [7, 15, 30]
# distances = [9, 40, 200]
times = [54, 81, 70, 88]
distances = [446, 1292, 1035, 1007]


def solve_quad(t, d):
    discriminant = t ** 2 - 4 * d
    if discriminant < 0:
        quad_sol = None
    elif discriminant == isqrt(discriminant) ** 2:
        quad_sol = (t - isqrt(discriminant)) / 2, (t + isqrt(discriminant)) / 2
    else:
        quad_sol = (t - sqrt(discriminant)) / 2, (t + sqrt(discriminant)) / 2
    return quad_sol


def find_range(t, d):
    roots = solve_quad(t, d)
    if roots is None:
        rng = 0
    else:
        rng = ceil(roots[1] - 1) - floor(roots[0] + 1) + 1
    return rng


print(f'Solution to Day 6 Problem 1 is {prod(find_range(time, distance) for time, distance in zip(times, distances))}')

time = int(''.join(str(t) for t in times))
distance = int(''.join(str(d) for d in distances))

print(f'Solution to Day 6 Problem 1 is {find_range(time, distance)}')