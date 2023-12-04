import re
from collections import defaultdict

with open("data/aoc_input_2023_4.txt") as file:
    file_contents = file.readlines()


def score_card(p_win_numbers, p_my_numbers):
    return len(p_win_numbers & p_my_numbers)


def calc_points(n):
    if n == 0:
        game_points = 0
    else:
        game_points = 2 ** (n-1)
    return game_points


winning_numbers = []
my_numbers = []

for line in file_contents:
    card, winning_chunk, my_chunk = re.split('[:|]', line)
    winning_numbers.append({int(n) for n in re.findall(r'\d+', winning_chunk)})
    my_numbers.append({int(n) for n in re.findall(r'\d+', my_chunk)})

scores = [score_card(win_nums, play_nums) for win_nums, play_nums in zip(winning_numbers, my_numbers)]

print(f'Solution to Day 4, Problem 1 is {sum(calc_points(score) for score in scores)}')

card_numbers = defaultdict(int)
for i, score in enumerate(scores, 1):
    card_numbers[i] += 1
    n = card_numbers[i]
    for j in range(1, score + 1):
        card_numbers[i+j] += n

print(f'Solution to Day 4, Problem 1 is {sum(card_numbers.values())}')


