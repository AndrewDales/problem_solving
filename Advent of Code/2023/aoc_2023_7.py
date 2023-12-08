import re
from collections import Counter

with open('data/aoc_input_2023_7.txt') as file:
    file_contents = file.read()


class CardSet:
    values = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10,
              '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 2}

    def __init__(self, cards, bid=0):
        self.cards = cards
        self.bid = bid

    @property
    def type(self):
        count_types = {(5,): 6, (4, 1): 5, (3, 2): 4, (3, 1, 1): 3, (2, 2, 1): 2, (2, 1, 1, 1): 1, (1,)*5: 0}
        counts = Counter(self.cards)
        count_nums = tuple(sorted(counts.values(), reverse=True))
        return count_types[count_nums]

    @property
    def value(self):
        return [self.type] + [self.values[card] for card in self.cards]

    def __gt__(self, other):
        return self.value > other.value

    def __eq__(self, other):
        return self.cards == other.cards

    def __repr__(self):
        return f'CardSet({self.cards})'


class CardSetJoker(CardSet):
    values = {'A': 14, 'K': 13, 'Q': 12, 'J': 1, 'T': 10,
              '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 2}

    @property
    def type(self):
        count_types = {(5,): 6, (4, 1): 5, (3, 2): 4, (3, 1, 1): 3, (2, 2, 1): 2, (2, 1, 1, 1): 1, (1,) * 5: 0}
        counts = Counter(self.cards)
        num_jokers = counts['J']
        if num_jokers < 5:
            del counts['J']
            max_card, _ = max(list(counts.items()), key=lambda x: (x[1], self.values[x[0]]))
            counts[max_card] += num_jokers
        count_nums = tuple(sorted(counts.values(), reverse=True))
        return count_types[count_nums]


card_set_list = []
card_set_list_jokers = []
for match in re.finditer(r'([A-Z|\d]{5}) (\d+)',file_contents):
    card_set_list.append(CardSet(match.group(1), int(match.group(2))))
    card_set_list_jokers.append(CardSetJoker(match.group(1), int(match.group(2))))

card_set_list.sort()

winnings = sum(i*card.bid for i, card in enumerate(card_set_list, 1))

print(f'Solution to Day 7, Problem 1 is {winnings}')

card_set_list_jokers.sort()
winnings_jokers = sum(i*card.bid for i, card in enumerate(card_set_list_jokers, 1))

print(f'Solution to Day 7, Problem 2 is {winnings_jokers}')