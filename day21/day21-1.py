from itertools import cycle, islice

p1_start_pos = 7
p2_start_pos = 9
track_length = 10
track = [10] + list(range(1, track_length))

d100 = cycle(range(1,101))

p1_score, p2_score = 0, 0
p1_pos, p2_pos = p1_start_pos, p2_start_pos
rolls = 0

while p1_score < 1000 and p2_score < 1000:
    if rolls % 2 == 0:
        p1_pos = (p1_pos + sum(islice(d100, 3))) % track_length
        p1_score += track[p1_pos]
    else:
        p2_pos = (p2_pos + sum(islice(d100, 3))) % track_length
        p2_score += track[p2_pos]

    rolls += 1

print(f'p1 score:{p1_score} p2 score:{p2_score} dice rolled:{rolls * 3}')