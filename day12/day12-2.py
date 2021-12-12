# this whole approach is wildly inefficient and
# should be re-written, but it got me the right answer and I 
# have other things to do today

from collections import defaultdict
from os import path
from typing import List, Set, Tuple

#file_to_use = 'day12/day12-sample.txt'
file_to_use = 'day12/day12-input.txt'

graph = defaultdict(set)
paths = set()
completed_paths = set()

paths_with_repeated_caves = set()
paths_to_caves = defaultdict(set)

def can_grow_to_neighbor(path, neighbor):
    if neighbor == 'end':
        return False
    elif neighbor[0].isupper():
        return True
    elif neighbor not in paths_to_caves[path]:
        return True
    #comment out if you want to verify you didn't break 12-1
    elif path not in paths_with_repeated_caves:
        return True
    return False

def grow_paths(path) -> Set[Tuple[str]]:
    new_paths = set()
    for neighbor in graph[path[-1]]:
        if can_grow_to_neighbor(path, neighbor):
            new = path + (neighbor,)
            new_paths.add(new)
            # TODO: investigate
            paths_to_caves[new] = set(new)
            if path in paths_with_repeated_caves \
                 or (neighbor[0].islower() and neighbor in paths_to_caves[path]):
                paths_with_repeated_caves.add(new)
    return new_paths


with open(file_to_use) as f:
    for line in [l.strip() for l in f]:
        a,b = line.split('-')
        graph[a].add(b)
        graph[b].add(a)

new_paths = set()
new_paths.add(('end',))

while len(new_paths) > 0:
    paths = new_paths
    new_paths = set()
    for p in frozenset(paths):
        if p[-1] != 'start':
            new_paths = new_paths.union(grow_paths(p))
        else:
            completed_paths.add(p)

print(f'{len(completed_paths)} for {file_to_use}')
