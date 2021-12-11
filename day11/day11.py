from os import X_OK
from typing import List, Type
import itertools

#file_to_use = 'day11/day11-sample.txt'
file_to_use = 'day11/day11-input.txt'

class Octopus:
    def __init__(self, x, y, energy, gridmap) -> None:
        self.x = x
        self.y = y
        self.energy = energy
        self.gridmap = gridmap
        self.neighbors = [(x-1,y-1), (x,y-1), (x+1,y-1),(x-1,y),(x+1,y),(x-1,y+1),(x,y+1), (x+1, y+1) ]

    def flash_neighbors(self):
        for n in self.neighbors:
            if n in self.gridmap:
                self.gridmap[n].energy += 1


with open(file_to_use) as f:
    y = 0
    gridmap = {}
    for line in [l.strip() for l in f]:
        x = 0
        for d in line:
            gridmap[(x,y)] = Octopus(x, y, int(d), gridmap)
            x += 1
        y += 1

steps_to_run = 100
flash_total = 0

i = 1
waiting_for_sync = True

while waiting_for_sync:
    flashers = set()
    for _, v in gridmap.items():
        v.energy += 1

    # I'm sure there's a very pretty recursive solution for this
    fc_prev = -1
    while fc_prev != len(flashers):
        fc_prev = len(flashers)
        for f in filter(lambda x: x.energy > 9, gridmap.values()):
            if f not in flashers:
                flashers.add(f)
                f.flash_neighbors()

    if i <= steps_to_run:
        flash_total += len(flashers)

    for flashed in flashers:
        flashed.energy = 0

    if len(flashers) == len(gridmap):
        waiting_for_sync = False
    else:
        i += 1

print(f'All octopi flashed on step {i}')
print(f'Flash total for {file_to_use} after {steps_to_run} is {flash_total}')