from collections import Counter

min_val = 357253
max_val = 892942


value_set = [(i, ) for i in range(3,9)]

for _ in range(5):
    value_set = [vs + (j,) for vs in value_set for j in range(vs[-1], 10)]

value_set = [vs for vs in value_set
             if ((3, 5, 7, 2, 5, 3) <= vs <= (8, 9, 2, 9, 4, 2)
                 and len(set(vs)) < len(vs))]

value_set_day_2 = [vs for vs in value_set
                   if 2 in Counter(vs).values()]

print(f'Solution to Day 4, problem 1 is {len(value_set)}')
print(f'Solution to Day 4, problem 2 is {len(value_set_day_2)}')
