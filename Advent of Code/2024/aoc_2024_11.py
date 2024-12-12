from functools import lru_cache

test_data = '125 17'
puzzle_data = '2 72 8949 0 981038 86311 246 7636740'

@lru_cache
def split_stones(n):
    if n == 0:
        return (1,)
    str_n = str(n)
    l = len(str_n)
    if l % 2 == 0:
        return (int(str_n[:l // 2]), int(str_n[l // 2:]))
    else:
        return (n * 2024, )

@lru_cache
def count_splits(n, num_splits=25):
    if num_splits == 0:
        return 1
    else:
        return sum(count_splits(i, num_splits-1) for i in split_stones(n))

initial_stones = list(map(int, puzzle_data.split(' ')))

print(f'Solution to Day 11a is {sum(count_splits(i) for i in initial_stones)}')
print(f'Solution to Day 11b is {sum(count_splits(i,75) for i in initial_stones)}')