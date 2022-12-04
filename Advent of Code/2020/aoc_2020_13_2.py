import re

with open("aoc_2020_13.txt") as file:
    current_time = int(file.readline().strip())
    line = file.readline().strip()
    nums = re.findall(r'[0-9]+', line)
    line_list = line.split(",")

bus_pairs = [(int(num), int(num) - line_list.index(num)) for num in nums]


def mod_inverse(a, p):
    return (a ** (p - 2)) % p


def calc_pair(pair_1, pair_2):
    p = pair_1[0]
    m = pair_1[1]
    q = pair_2[0]
    n = pair_2[1]
    a = (n - m) * mod_inverse(p % q, q) % q
    return p * q, a * p + m

orig_pairs = bus_pairs.copy()
p1 = bus_pairs.pop(0)

while bus_pairs:
    p2 = bus_pairs.pop(0)
    p1 = calc_pair(p1, p2)
    print(p1)

print(f'Solution to part 2 is {p1[1]}')
