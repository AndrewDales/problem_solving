from collections import deque

with open("aoc_input_2021_12.txt", "r") as file:
    connections = set(frozenset(line.strip().split("-")) for line in file)
    
nodes = set(el for fs in connections for el in fs)

path_stack = deque([('start',)])
finished_routes = []

while path_stack:
    current_path = path_stack.popleft()
    last_node = current_path[-1]
    # If 
    if last_node == "end":
        finished_routes.append(current_path)    
    else: 
        # Find the linked pairs in connections that contain the last_node,
        # Then take last_node out of the pair, and pop the other element out of the pair
        neighbours = set(set(linked_pair - {last_node}).pop()
                         for linked_pair in connections
                         if last_node in linked_pair)
        
        # Take out the lower case nodes from neighbours if they are already in the current path
        neighbours = neighbours - set(node for node in current_path if node.islower())
        
        for neighbour in neighbours:
            path_stack.append(current_path + (neighbour,))

print(f"Output Solution, number of possible routes = {len(finished_routes)}")