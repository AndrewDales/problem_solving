from itertools import pairwise
from collections import Counter

with open("aoc_input_2021_14.txt", "r") as file:
    starting_code = file.readline().strip()
    # Skip an empty line
    file.readline()
    code_dict = {line[:2] : line.strip()[-1] for line in file}
    

class Polymer:
    def __init__(self, start_code, insert_dict):
        self.code = start_code
        self.insert_dict = insert_dict
        # self.pairs are the continous pairs in start_code
        self.pairs = Counter(p0 + p1 for p0, p1 in pairwise(self.code))
        
    def insert_into_pairs(self):
        new_pairs = Counter()
        # Go through each pair, for each pair split it into two with the looked up insert_letter.
        # Update the counter with the number of each of the new pairs produced.
        for pair, num_pair in self.pairs.items():
            insert_letter = self.insert_dict[pair]
            new_pairs.update(Counter({pair[0]+insert_letter: num_pair, insert_letter + pair[1]: num_pair}))
        self.pairs = new_pairs
                                                                            
    def insertion_steps(self, num_steps):
        for _ in range(num_steps):
            self.insert_into_pairs()
            
    def max_min_score(self):
        # Counting the leeters in each pair will double count every letter except the first and last,
        # so add an extra count of the first and last letters in the original code.
        letter_counter = Counter({self.code[0]: 1, self.code[-1]: 1})
        for pair, num in self.pairs.items():
            letter_counter.update(Counter({pair[0]: num}))
            letter_counter.update(Counter({pair[1]: num}))       
        
        letter_count = letter_counter.most_common()
        return letter_count[0][1]//2 - letter_count[-1][1]//2
        
        
        
poly = Polymer(starting_code, code_dict)
# poly.insert_into_pairs()
poly.insertion_steps(40)

print(f"Output Solution 2: {poly.max_min_score()}")
