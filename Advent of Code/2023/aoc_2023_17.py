from dataclasses import dataclass
from queue import PriorityQueue

with open('data/aoc_input_2023_17.txt') as file:
    file_contents = [line.strip() for line in file.readlines()]
    LAVA_MAP = {(row, col): int(digit)
                for row, line in enumerate(file_contents)
                for col, digit in enumerate(line)}

N_ROWS = len(file_contents)
N_COLS = len(file_contents[0])
DIRECTIONS = {'N': (-1, 0),
              'S': (1, 0),
              'E': (0, 1),
              'W': (0, -1,
                    )}
OPPOSITE_DIRECTIONS = {'N': 'S', 'E': 'W', 'S': 'N', 'W': 'E'}


def is_inside(location):
    return 0 <= location[0] < N_ROWS and 0 <= location[1] < N_COLS


def neighbours(location):
    return {compass: new_loc for compass, direction in DIRECTIONS.items()
            if is_inside(new_loc := (location[0] + direction[0], location[1] + direction[1]))}


@dataclass(frozen=True)
class Node:
    location: tuple[int, int]
    path: str = ''
    cost: int = 0

    @property
    def neighbours(self):
        excludes = set()
        if self.path:
            excludes.add(OPPOSITE_DIRECTIONS[self.path[-1]])
        if len(self.path) >= 3 and self.path[-1] == self.path[-2] and self.path[-1] == self.path[-3]:
            excludes.add(self.path[-1])
        node_neighbours = {c: d for c, d in neighbours(self.location).items() if c not in excludes}
        return node_neighbours

    def dist_in_direction(self):
        count = 0
        if self.path:
            last = self.path[-1]
            for i, path_letter in enumerate(reversed(self.path), 1):
                if path_letter != last:
                    count = i - 1
                    break
            else:
                count = len(self.path)
        return count

    def neighbours_part_2(self):
        valid_directions = set(DIRECTIONS)
        if self.path:
            current_direction = self.path[-1]
            valid_directions = valid_directions - {current_direction, OPPOSITE_DIRECTIONS[current_direction]}

        neighbour_nodes = []
        for vd in valid_directions:
            loc = self.location
            cost = self.cost
            path = self.path
            cur_dir = DIRECTIONS[vd]
            for i in range(1, 11):
                loc = (loc[0] + cur_dir[0], loc[1] + cur_dir[1])
                if not is_inside(loc):
                    break
                cost += LAVA_MAP[loc]
                path += vd
                if i >= 4:
                    neighbour_nodes.append(Node(loc, path=path, cost=cost))
        return neighbour_nodes

    def signature(self, part):
        if part == 1:
            sig = self.location, self.path[-3:]
        else:
            sig = self.location, self.path[-1:]
        return sig

    def next_node(self, direction, part=1):
        if part == 1:
            new_location = self.neighbours[direction]
        else:
            new_location = self.neighbours_part_2()[direction]
        return Node(new_location, path=self.path + direction, cost=self.cost + LAVA_MAP[new_location])

    def neighbour_nodes(self, part=1):
        if part == 1:
            n_nodes = [self.next_node(d, part) for d in self.neighbours]
        else:
            n_nodes = self.neighbours_part_2()
        return n_nodes

    def __lt__(self, other):
        return self.cost < other.cost


def calc_distance_to_end(end_location=(N_ROWS - 1, N_COLS-1)):
    priority_queue = PriorityQueue()
    unvisited = {(i, j) for i in range(N_ROWS) for j in range(N_ROWS)}
    visited = {}
    current_loc = end_location
    current_cost = 0

    while unvisited:
        visited[current_loc] = current_cost
        unvisited.remove(current_loc)
        for _, ngh in neighbours(current_loc).items():
            if ngh not in visited:
                priority_queue.put((LAVA_MAP[current_loc] + current_cost, ngh))
        new_item = False
        while not new_item and not priority_queue.empty():
            current_cost, current_loc = priority_queue.get()
            if current_loc in unvisited:
                new_item = True

    return visited


def calc_min_path(start_node: Node, end_loc, heuristic, part=1):
    priority_queue = PriorityQueue()
    visited = set()
    current_node = start_node

    while current_node.location != end_loc:
        visited.add(current_node.signature(part))
        for ngh in current_node.neighbour_nodes(part):
            if ngh.signature(part) not in visited:
                approx_cost = ngh.cost + heuristic[ngh.location]
                priority_queue.put((approx_cost, ngh))
        if priority_queue.empty():
            raise IndexError('No more items in priority queue')
        new_item = False
        while not new_item:
            current_cost, current_node = priority_queue.get()
            if current_node.signature(part) not in visited:
                new_item = True
        # print(current_node.signature(part))
    return current_node, visited


unconstrained_distance = calc_distance_to_end()

print('Finished Heuristic')

start = Node((0, 0))
end_path, paths = calc_min_path(start, (N_ROWS-1, N_COLS-1), unconstrained_distance, part=1)

print(f'Solution to Day 17, Problem 1 is {end_path.cost}')

end_path, paths = calc_min_path(start, (N_ROWS-1, N_COLS-1), unconstrained_distance, part=2)

print(f'Solution to Day 17, Problem 2 is {end_path.cost}')
