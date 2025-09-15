import turtle
from l_system import l_system, draw_sequence

dragon_rules = {'F': 'F+G',
                'G': 'F-G',
                }

dragon_seed = 'F'

side_length = 2
dragon_commands = {'F': lambda : turtle.forward(side_length),
                   'G': lambda : turtle.forward(side_length),
                   '+': lambda : turtle.left(90),
                   '-': lambda : turtle.right(90),
                   }

dragon_sequence = l_system(12, dragon_seed, dragon_rules)

draw_sequence(dragon_sequence, dragon_commands, position=(0,0))