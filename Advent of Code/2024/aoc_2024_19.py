import re
from functools import lru_cache

with open('data/aoc_input_2024_19.txt') as file:
    file_contents = file.read()

file_contents = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb"""

file_patterns, file_towels = file_contents.split('\n\n')

patterns = set(file_patterns.split(', '))
towels = file_towels.split()

def match_pattern(towel, t_patterns):
    return {(pattern, towel[len(pattern):])  for pattern in t_patterns if towel.startswith(pattern)}

# @lru_cache(maxsize=None)
# def bfs_towel(towel):
#     pattern_matches = match_pattern(towel, patterns)
#     for _, r_towel in pattern_matches:
#         if not r_towel:
#             return True
#         else:
#             if bfs_towel(r_towel):
#                 return True
#     return False

# @lru_cache(maxsize=None)
def bfs_towel(towel):
    pattern_matches = match_pattern(towel, patterns)
    for pattern, r_towel in pattern_matches:
        if not r_towel:
            yield pattern
            return True
        else:
            pattern_sequence = tuple(bfs_towel(r_towel),)
            if pattern_sequence:
                yield pattern_sequence + (pattern,)
                return True
    return False

# for seq in bfs_towel('r'):
#     print(seq)

for seq in bfs_towel(towels[0]):
    print(seq)

# n_towel_matches = 0
# matching_towels = []
# for i, towel in enumerate(towels):
#     towel_match = bfs_towel(towel)
#     if towel_match:
#         matching_towels.append(towel)
#         n_towel_matches += 1
#     print(i)
#
# print(f'Solution to 19a is {n_towel_matches}')