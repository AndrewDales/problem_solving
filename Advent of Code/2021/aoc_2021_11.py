import numpy as np
from collections import deque

# Opens the file of lines of digits. Converts each line into a list of digits
# then puts all the lines into a numpy array of integers
with open("aoc_input_2021_11.txt", "r") as file:
    data = np.array([list(line.strip()) for line in file], int)
    
    
class Octopus_Grid:
    flash_level = 10
    
    def __init__(self, energy_level):        
        self.energy_level = np.array(energy_level)
        self.flashed = set()
        self.flash_queue = deque()
        self.round_flashes = 0
        self.total_flashes = 0
        self.current_round = 0
        
    def get_neighbours(self, index):
        directions = np.array([[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]])
        neighbours = [tuple(index + direction) for direction in directions
                      if (all((0, 0) <= index + direction) and
                          all(index + direction < data.shape))]                     
        return neighbours
        
    def flash(self, index):
        neighbours = self.get_neighbours(index)
        for neighbour in neighbours:
            # Increase levels of a neighbour that has not already flashed by one
            if self.energy_level[neighbour] < self.flash_level and (tuple(neighbour) not in self.flashed):
                self.energy_level[neighbour] += 1
                # Add the cell index of any neighbour reaching the flash_level to the flash queue
                if self.energy_level[neighbour] == self.flash_level:
                    self.flash_queue.append(neighbour)
        # Add the index to the set of tuples that have flashed and set the energy_level to 0
        self.flashed.add(index)
        self.energy_level[index] = 0
        self.round_flashes += 1
        
    def step(self, num_steps = 1):
        for current_round in range(num_steps):
            self.flashed = set()
            self.round_flashes = 0
            self.energy_level += 1
            # Create a queue of coords to be flashed. We need to transpose the array to get [x, y] pairs
            self.flash_queue = deque(np.transpose((self.energy_level >= self.flash_level).nonzero())) 
            while self.flash_queue:
                flash_index = self.flash_queue.popleft()
                self.flash(tuple(flash_index))
            self.current_round += 1
            self.total_flashes += self.round_flashes
    
    def all_flash(self):
        while self.round_flashes < self.energy_level.size:
            self.step()
            print(self.current_round, self.round_flashes)
        
    
    def __repr__(self):
        return f'Octopus_Grid(\n{str(self.energy_level)}\n)'        
        
    
if __name__ == "__main__":
    grid = Octopus_Grid(data)
    grid.step(100)
    print(f"Output Solution, num flashes = {grid.total_flashes}")
    grid.all_flash()
    print(f"Output Solution, part 2 = {grid.current_round}")
