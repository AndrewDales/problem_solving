# Advent of Code

*Spoiler alert*. This repo contains solutions to problems from the [Advent of Code](https://adventofcode.com/) problem set. This is a great problem-solving resource that I have used with Secondary School pupils at [Highgate School](https://www.highgateschool.org.uk/)

## Solution code and data
Many of the [Advent of Code](https://adventofcode.com/) problems illustrate standard Computer Science theory. Here are some examples of Computer Science topic areas and Python techniques that I used for my solutions.
- [2020](https://github.com/AndrewDales/advent_of_code/tree/main/Advent%20of%20Code/2020)
  - Day 3: Use `defaultdict(int)` to set up a labelled counter that will automatically start at zero.
  - Day 4: Use [regex](https://en.wikipedia.org/wiki/Regular_expression) to recognise a valid hex colour code. `^#[A-Fa-f0-9]{6}$` matches a hex colour code such as #ee45a5.
  - Day 6: Use `my_set[0].intersection(*my_set[1:])` to find the intersection of a list of sets.
  - Day 7: This problem involves a [tree](https://en.wikipedia.org/wiki/Tree_(data_structure)) structure.
    - Use [regex](https://en.wikipedia.org/wiki/Regular_expression) to help parse each line, including `re.findall('re.findall(r'[0-9]+', my_string')` to find all the numbers in a string
    - Use a [recursive depth first search](https://www.techiedelight.com/depth-first-search/) to traverse the tree.
  - Day 8: The problem involves a program written in a simple assembly language with jump (goto) statements and an accumulator.
    - I used a State `dataclass` from the `dataclasses` module to keep track of the current state of a program run.
  - Day 10: Solved using a [recurrence relation](https://en.wikipedia.org/wiki/Recurrence_relation)
  - Day 11: This is an example of a 2D [cellular automaton](https://en.wikipedia.org/wiki/Cellular_automaton)
    - Solved by using a `dataclass` to hold the current state and transitioning each cell depending on the transition rules
    - Solution involved writing a `find_neighbour` function to find all the neighbours of a given cell in an n-dimensional grid.
  - Day 13: This requires solving linear modulo equations. Some [modulo maths](https://www.omnicalculator.com/math/chinese-remainder#example-using-the-chinese-remainder-theorem) is required, but with this to hand, the programming is easy.
- [2021](https://github.com/AndrewDales/advent_of_code/tree/main/Advent%20of%20Code/2021)
- [2022](https://github.com/AndrewDales/advent_of_code/tree/main/Advent%20of%20Code/2022)
  - Day 3: Use `set` and `intersection`
  - Day 5: Explores the concept of the [stack](https://en.wikipedia.org/wiki/Stack_(abstract_data_type))
    - Parsing the data was fiddly
    - I used `defaultdict` and `namedtuple` from the `collections` module to hold data.
  - Day 6: This problem is about recognising when the data from a signal starts. With [serial data transmission](https://learn.sparkfun.com/tutorials/serial-communication/all) a start bit is required to define when the data begins. 
  - Day 7: The hardest challenges so far. This involved making a [tree structure](https://en.wikipedia.org/wiki/Tree_(data_structure)) from file directory information.
    - I created a separate `dataclass` for files and directories. 
    - `ls` and `cd` commands cound be read from the list of instructions and used to create files and directories with parents and children
    - A tree traversal was required to find the sizes of all the files contained in each directory
  - Day 10: A simulation of a CPU clock with actions taking one or two clicks on the clock. The second part of the problem also involves a monitor drawing one pixel at each click on the clock.
- [2023](https://adventofcode.com/2023)
  - Day 1: Trickier than usual. A good case to practice using regular expressions to find all the digit matches ([re](https://docs.python.org/3/library/re.html)). I got stuck on the second part for quite a while before noticing that some of the word strings overlap. E.g. in the example 'eightwothree' where 'eight' and 'two' share the 't'. The problem is that regular expressions are 'greedy', hence when they match 'eight', they have used up the 't' and won't match the 'two'. Googling 'overlapping regular expressions' took me [here](https://mtsknn.fi/blog/how-to-do-overlapping-matches-with-regular-expressions/), which explains 'lookahead' and 'lookbehind' regular expressions. These expressions don't consume the tokens, but instead look ahead (or behind) and match an expression if the tokens ahead of the cursor match the re. 
    - Example: `re.findall(r'(?=([a-e][a-e]))', 'abcde')` returns `['ab', 'bc', 'cd', 'de']`, whereas `re.findall(r'([a-e][a-e])', 'abcde')` only returns `['ab', 'cd']`
### Andrew Dales
