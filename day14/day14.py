from collections import defaultdict
from itertools import tee

# I don't have python 3.10 here
def pairwise(iterable):
    # pairwise('ABCDEFG') --> AB BC CD DE EF FG
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

#file_to_use = 'day14/day14-sample.txt'
file_to_use = 'day14/day14-input.txt'
steps_to_take = 40

pair_counts = defaultdict(int)
letter_counts = defaultdict(int)
insertion_rules = dict()

with open(file_to_use) as f:
    line = f.readline().strip()
    for pair in pairwise(line):
        pair_counts[pair] += 1
    # ends up with weird counts at the start and end of the list. Adjust as needed
    letter_counts[line[0]] = .5
    letter_counts[line[-1]] = .5
    _ = f.readline()
    line = f.readline().strip()
    while line != '':
        insertion_rules[(line[0], line[1])] = [(line[0], line[-1]), (line[-1], line[1])]
        line = f.readline().strip()

for i in range(steps_to_take):
    new_pair_counts = defaultdict(int)
    for p,c in pair_counts.items():
        if p in insertion_rules:
            for new_pair in insertion_rules[p]:
                new_pair_counts[new_pair] += c
        else:
            new_pair_counts[p] += c
    pair_counts = new_pair_counts

for p,c in pair_counts.items():
    letter_counts[p[0]] += c / 2
    letter_counts[p[1]] += c / 2

max_letter = max(letter_counts, key=letter_counts.get)
min_letter = min(letter_counts, key=letter_counts.get)

print(f'{letter_counts[max_letter] - letter_counts[min_letter]}')
