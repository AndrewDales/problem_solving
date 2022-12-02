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

def rps_score_2(p1_obj, p2_obj):
    p2_obj_scores = {"X": 1, "Y": 2, "Z": 3}
    draw_table = {"A": "X", "B": "Y", "C": "Z"}
    win_table = {"A": "Y", "B": "Z", "C": "X"}
    lose_table = {"A": "Z", "B": "X", "C": "Y"}
    
    p2_score = 0
    
    # require loss
    if p2_obj == "X":
        play_obj = lose_table[p1_obj]
    
    # require draw
    elif p2_obj == "Y":
        play_obj = draw_table[p1_obj]
        p2_score += 3
        
    # rerquire win
    elif p2_obj == "Z":
        play_obj = win_table[p1_obj]
        p2_score += 6
    

    p2_score += p2_obj_scores[play_obj]
    return p2_score

print(sum(rps_score_2(p1, p2) for p1, p2 in moves))
    