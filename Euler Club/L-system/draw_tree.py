import turtle
import turtleBeads

from l_system import l_system, draw_sequence

side_length = 5
depth = 5

screen = turtle.Screen()
screen.setup(width=1.0, height=1.0)

# Set the rules for your lindenmeyer systems
commands = {'F': lambda : turtle.forward(side_length),
                   '+': lambda : turtle.left(22.5),
                   '-': lambda : turtle.right(22.5),
                   }

rules = {'F': 'FF+[+F-F-F]-[-F+F+F]',
                }
seed = 'F'

turtleBeads.noTrace()
sequence = l_system(depth, seed, rules)
screen.bgcolor('black')
turtle.pencolor('yellow')
turtleBeads.noTrace()
draw_sequence(sequence, commands)
turtle.hideturtle()
turtleBeads.showPicture()
turtle.done()

turtleBeads.showPicture()
turtle.done()