import turtle
from l_system import l_system

side_length = 10

dragon_commands = {'F': lambda : turtle.forward(side_length),
                   'G': lambda : turtle.forward(side_length),
                   '+': lambda : turtle.left(90),
                   '-': lambda : turtle.right(90),
                   }

dragon_rules = {'F': 'F+G',
                'G': 'F-G',
                }

dragon_seed = 'F'


dragon_sequence = l_system(9, dragon_seed, dragon_rules)

tree_rules = {'1': '11',
              '0': '1[+0]-0',
              }

tree_seed = '0'
tree_sequence = l_system(2, tree_seed, tree_rules)

print(tree_sequence)