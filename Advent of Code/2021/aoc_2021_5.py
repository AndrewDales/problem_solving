class Grid:
    def __init__(self, n_x, n_y):
        self.values = [[0] * n_x for _ in range(n_y)]
    
    def add_line(self, line, line_type="straight"):
        lines = line.straight_lines
        if line_type == "all":
            lines += line.diagonal_lines
        for x, y in lines:
            self.values[y][x] += 1
    
    def count_points(self, min_value = 2):
        return sum(True for row in self.values for el in row if el >= 2) 

class Line:
    def __init__(self, start_point, end_point):
        self.start_point = start_point
        self.end_point = end_point
        
    @staticmethod
    def _get_range(a, b):
        if a < b:
            inc_range = range(a, b+1, 1)
        else:
            inc_range = range(a, b-1, -1)
        return inc_range
        
    @property
    def straight_lines(self):
        if (x:= self.start_point[0]) == self.end_point[0]:
            y0, y1 = self.start_point[1], self.end_point[1]
            lines = [(x, i) for i in range(min(y0, y1), max(y0,y1)+1)]
        elif (y:= self.start_point[1]) == self.end_point[1]:
            x0, x1 = self.start_point[0], self.end_point[0]
            lines = [(i, y) for i in range(min(x0, x1), max(x0, x1)+1)]
        else:
            lines = []
        return lines
    
    @property
    def diagonal_lines(self):
        if abs(self.start_point[0] - self.end_point[0]) == abs(self.start_point[1] - self.end_point[1]):
            x_range = self._get_range(self.start_point[0], self.end_point[0])
            y_range = self._get_range(self.start_point[1], self.end_point[1])
            lines = [(i,j) for i,j in zip(x_range, y_range)]
        else:
            lines = []
        return lines
            

with open("aoc_input_2021_5.txt", "r") as file:
    lines = []
    max_x = 0
    max_y = 0
    for line in file:
        coord_row = line.replace(" ","").split("->")
        coord = tuple(tuple(int(el) for el in row.split(",")) for row in coord_row)
        lines.append(Line(*coord))
        max_x = max(max_x, coord[0][0], coord[1][0])
        max_y = max(max_y, coord[0][1], coord[1][1])
        
grid = Grid(max_x+1, max_y+1)
for line in lines:
    grid.add_line(line)
    
print(f"Output solution part 1: {grid.count_points(2)}")

grid_2 = Grid(max_x+1, max_y+1)
for line in lines:
    grid_2.add_line(line, "all")
    
print(f"Output solution part 2: {grid_2.count_points(2)}")