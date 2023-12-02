import re
from math import prod

with open("data/aoc_input_2023_2.txt") as file:
    file_contents = file.readlines()

MAX_VALUES = {'red': 12,
              'green': 13,
              'blue': 14}

# Put the list of numbers for each colour in a dictionary


numbers = {i: {color: [int(val) for val in re.findall(rf'(\d+) {color}', line)]
               for color in MAX_VALUES}
           for i, line in enumerate(file_contents, 1)
           }

max_per_game = {game: {color: max(numbers[game][color]) for color in numbers[game]} for game in numbers}

possible_games = [game_number for game_number, game_draws in max_per_game.items()
                  if all(game_draws[color] <= MAX_VALUES[color] for color in MAX_VALUES)]
power_per_game = [prod(game.values()) for game in max_per_game.values()]

print(f'Solution to Day 2, Part 1 is {sum(possible_games)}')
print(f'Solution to Day 2, Part 2 is {sum(power_per_game)}')
