from statistics import median

with open("aoc_input_2021_10.txt", "r") as file:
    data = [line.strip() for line in file]
    
def check_line(line: str):
    bracket_closers = {')':'(', ']':'[', '}':'{', '>':'<'}
    bracket_stack = []
    output = None
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
    # Gets to the end of the line without wrong bracket
    else:
        if line:
            output = "".join(bracket_stack)
    
    return output

def score_closures(line: str):
    bracket_scores = {')': 1, ']': 2, '}': 3, '>': 4}
    score = 0
    for el in line:
        score = score * 5 + bracket_scores[el]
    return score

def close_bracket_string(open_brackets: str) -> str:
    bracket_match = {'(':')', '[':']', '{':'}', '<':'>'}
    return "".join([bracket_match[bk] for bk in open_brackets[::-1]])

if __name__ == "__main__":
    completions = [close_bracket_string(unclosed_line)
                   for chunk in data
                   if (unclosed_line:= check_line(chunk))]
    completion_scores = [score_closures(completion) for completion in completions]
    
    print(f"Output Solution, Part 2 = {median(completion_scores)}")