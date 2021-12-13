from collections import namedtuple
from typing import NamedTuple

Fold = namedtuple('Fold', 'axis loc')
Dot = namedtuple('Dot', 'x y')

#file_to_use = 'day13/day13-sample.txt'
file_to_use = 'day13/day13-input.txt'

grid = set()
folds = []

with open(file_to_use) as f:
    l = f.readline().strip()
    while l != '':
        x, y = l.split(',')
        grid.add(Dot(int(x), int(y)))
        l = f.readline().strip()
    l = f.readline().strip()
    while l != '':
        axis,loc = l.split('=')
        folds.append(Fold(axis[-1], int(loc)))
        l = f.readline().strip()

# for 13-1, we do one fold, for 13-2 we do all of them
for fold in folds:
    for dot in frozenset(grid):
        if fold.axis == 'x' and dot.x > fold.loc or fold.axis == 'y' and dot.y > fold.loc:
            grid.remove(dot)
            if fold.axis == 'x':
                grid.add(Dot((fold.loc - dot.x) + fold.loc, dot.y))
            if fold.axis == 'y':
                grid.add(Dot(dot.x, (fold.loc - dot.y) + fold.loc))

for y in range(10):
    line = [' ' for i in range(40)]
    for dot in filter(lambda x : x.y == y, grid):
        line[dot.x] = '*'
    print(''.join(line))