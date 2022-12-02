with open("aoc_2022_2.txt", "r") as file:
    moves = [line.strip().split() for line in file]
    
def rps_score(p1_obj, p2_obj):
    p2_obj_scores = {"X": 1, "Y": 2, "Z": 3}
    p2_score = p2_obj_scores[p2_obj]
    
    if ((p1_obj == "A" and p2_obj == "Y") or
        (p1_obj == "B" and p2_obj == "Z") or
        (p1_obj == "C" and p2_obj == "X")):
        
        p2_score += 6
    
    if ((p1_obj == "A" and p2_obj == "X") or
        (p1_obj == "B" and p2_obj == "Y") or
        (p1_obj == "C" and p2_obj == "Z")):
        
        p2_score += 3
    
    return p2_score

print(sum(rps_score(p1, p2) for p1, p2 in moves))
    