from collections import defaultdict

vote_counter = defaultdict(int)

with open('PCTC 2022 R2 Q8.txt', 'r') as my_file:
    num_lines = int(my_file.readline())

    for _ in range(num_lines):
        line = my_file.readline()
        name, vote = line.strip().split(':')
        vote_dir, vote_name = vote.split(' ')
        if vote_dir == "DOWN":
            vote_counter[vote_name] -= 1
        elif vote_dir == "UP":
            vote_counter[vote_name] += 1

min_votes = min(vote_counter.values())

excludes = sorted([name for name, votes in vote_counter.items() if votes == min_votes])
print(excludes)

