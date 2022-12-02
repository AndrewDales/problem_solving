from itertools import pairwise
from collections import Counter

with open("aoc_input_2021_14_trial.txt", "r") as file:
    starting_code = file.readline().strip()
    # Skip an empty line
    file.readline()
    code_dict = {line[:2] : line.strip()[-1] for line in file}
    

class Polymer:
    def __init__(self, start_code, insert_dict):
        self.code = start_code
        self.insert_dict = insert_dict
        
    def insertion(self):
        first_and_insert = [p0 + self.insert_dict[p0+p1]
                             for p0, p1 in pairwise(self.code)]
        self.code = "".join(first_and_insert) + self.code[-1]
        
    def insertion_steps(self, num_steps):
        for _ in range(num_steps):
            self.insertion()
            
    def max_min_score(self):
        # Counter.most_common() lists the items in tuples from most to least likely
        letter_count = Counter(self.code).most_common()
        return letter_count[0][1] - letter_count[-1][1]
        
        
        
poly = Polymer(starting_code, code_dict)
poly.insertion_steps(10)

print(f"Output Solution 1: {poly.max_min_score()}")

poly.insertion_steps(30)

print(f"Output Solution 1: {poly.max_min_score()}")