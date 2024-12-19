import re
from functools import lru_cache

with open('data/aoc_input_2024_19.txt') as file:
    file_contents = file.read()

# file_contents = """r, wr, b, g, bwu, rb, gb, br
#
# brwrr
# bggr
# gbbr
# rrbgbr
# ubwu
# bwurrg
# brgr
# bbrgwb"""

file_patterns, file_towels = file_contents.split('\n\n')

patterns = set(file_patterns.split(', '))
towels = file_towels.split()

def match_pattern(towel, t_patterns):
    return {(pattern, towel[len(pattern):])  for pattern in t_patterns if towel.startswith(pattern)}

@lru_cache(maxsize=None)
def dfs_towel(towel):
    pattern_matches = match_pattern(towel, patterns)
    num_matches = 0
    for pattern, r_towel in pattern_matches:
        if not r_towel:
            num_matches += 1
        else:
            num_matches += dfs_towel(r_towel)
    return num_matches


match_ways = [dfs_towel(t) for t in towels]

print(f'Solution to 19a is {sum(m > 0 for m in match_ways)}')
print(f'Solution to 19b is {sum(match_ways)}')