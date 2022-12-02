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
        self.adjacent_cells = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
    def dijkstra(self):
        visited = {}
        priority_queue = [(0, self.start)]
        
        while not self.end in visited:
            current_item = heapq.heappop(priority_queue)
            current_cell = current_item[1]
            if current_cell in visited:
                continue
            current_cost = current_item[0]
            neighbours = [np.array(current_cell) + adj_cell
                          for adj_cell in self.adjacent_cells]
            neighbours = [tuple(point) for point in neighbours
                          if all((0,0) <= point) and
                          all(point <= self.end) and
                          tuple(point) not in visited]
            for neighbour in neighbours:
                heapq.heappush(priority_queue, (current_item[0] + self.data[neighbour], neighbour))
            visited[current_cell] = current_cost
        return visited, priority_queue    
        

cave = CaveSearch(cave_data)
visited, priority_queue = cave.dijkstra()

print(f"Output solution, part 1 = {visited[cave.end]}")