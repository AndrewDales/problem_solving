from collections import defaultdict

with open("aoc_input_2021_10_trial.txt", "r") as file:
    data = [line.strip() for line in file]
    
def check_line(line: str):
    bracket_closers = {')':'(', ']':'[', '}':'{', '>':'<'}
    bracket_stack = []
    for char in line:
        # if char is an open bracket add it to the stack
        if char in bracket_closers.values():
            bracket_stack.append(char)
        # Unmatched closing brackets after all preceeding brackets have closed
        elif len(bracket_stack) == 0:
            false_char = char
            break
        # Closing bracket matches open bracket at end of stack
        elif bracket_closers[char] == bracket_stack[-1]:
            bracket_stack.pop()
        # Closing bracket does not match bracket at end of stack
        else:
            false_char = char
            break
    else:
        false_char = None
    return false_char

bracket_scores = {')': 3, ']': 57, '}': 1197, '>': 25137}

if __name__ == "__main__":
    bad_closers = [bad_char for chunk in data if (bad_char:= check_line(chunk))]
    score = sum(bracket_scores[bad_char] for bad_char in bad_closers)
    print(f"Output Solution, Part 1 = {score}")