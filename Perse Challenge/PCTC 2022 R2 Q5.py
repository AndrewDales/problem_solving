# Q5 Rock Paper Scissors Wand

rounds = []

for _ in range(6):
    rounds.append(input())

scores = [0, 0]
wand_winner = None

for rnd in rounds:
    if rnd in ('RS', 'SP', 'PR'):
        scores[0] += 1
    elif rnd in ('SR', 'PS', 'RP'):
        scores[1] += 1
    elif rnd == "WW":
        if wand_winner in (0, 1):
            scores[wand_winner] = 0
    elif 'W' in rnd:
        w_index = rnd.index('W')
        scores[w_index] += 1
        wand_winner = w_index

print(f'{scores[0]}-{scores[1]}')
