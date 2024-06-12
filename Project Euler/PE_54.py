from collections import Counter

FILENAME = "poker.txt"
hands = []

with open(FILENAME, 'r') as file:
    for line in file:
        line = line.strip()
        line = line.split(' ')
        cards = [(card[0], card[1]) for card in line]
        hands.append(cards)
 
hand_types = {0: "High Card",
              1: "One Pair",
              2: "Two Pairs",
              3: "Three of a Kind",
              4: "Straight",
              5: "Flush",
              6: "Full House",
              7: "Four of a Kind",
              8: "Straight Flush",
              }
 
hand_shapes = {(4, 1): 7,
               (3, 2): 6,
               (3, 1, 1): 3,
               (2, 2, 1): 2,
               (2, 1, 1, 1): 1,
               (1, 1, 1, 1, 1): 0
               }
 
def find_shape(hand):
    ranks = [hand[0] for hand in hands]
    rank_counter = Counter(ranks)
    hand_shape = sorted(list(rank_counter.values))
    return hand_shapes(tuple(hand_shape))
    