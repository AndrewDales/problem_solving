import numpy as np
import heapq

with open("aoc_input_2021_15.txt", "r") as file:
    cave_data = np.array([[int(el) for el in line.strip()] for line in file])

class CaveSearch:
    def __init__(self, data):
        self.data = data
        self.start = (0, 0)
        n_rows, n_cols = self.data.shape
        self.end = (n_rows-1, n_cols-1)
        self.adjacent_cells = [(0, 1), (1, 0)]
        self.big_data = []
        self.make_big_matrix()
        # Costs nothing to enter the first cell
        self.big_data[0, 0] = 0
        self.n = self.big_data.shape[0]
        
    def make_big_matrix(self):
        self.big_data = self.data
        for i in range(1, 5):
            new_data = (self.data + i - 1) % 9 + 1
            self.big_data = np.hstack((self.big_data, new_data))
        h_stack_data = self.big_data
        for j in range(1, 5):
            new_data = (h_stack_data + j - 1) % 9 + 1
            self.big_data = np.vstack((self.big_data, new_data))
    
    def make_diag(self,i):
        n = self.big_data.shape[0]
        d = (tuple(i-j for j in range(i+1) if j<n and i-j<n),
             tuple(j for j in range(i+1) if j<n and i-j<n))
        return d    
     
    # Find the total cost diagonal by diagonal, by finding the minimum cost of total cost
    # of the cell above and to the left and adding on the cost of entering the new cell.
    def find_total_cost(self):
        total_cost = np.zeros(self.big_data.shape, dtype = int)
        total_cost[0,:] = np.cumsum(self.big_data[0, :])
        total_cost[:,0] = np.cumsum(self.big_data[:, 0])
        for d in range(2, 2*self.n):
            prev_total_cost = total_cost[self.make_diag(d-1)]
            diag_cells = self.make_diag(d)
            new_costs = self.big_data[diag_cells]
            if d < self.n:
                new_total_cost = np.min(np.vstack((prev_total_cost[:-1], prev_total_cost[1:])), axis=0) + new_costs[1:-1]
                total_cost[(diag_cells[0][1:-1], diag_cells[1][1:-1])] = new_total_cost
            else:
                new_total_cost = np.min(np.vstack((prev_total_cost[:-1], prev_total_cost[1:])), axis=0) + new_costs
                total_cost[diag_cells] = new_total_cost
                
        return total_cost
        
        

        

cave = CaveSearch(cave_data)
total_costs = cave.find_total_cost()


print(f"Output solution, part 2 = {total_costs[-1, -1]}")