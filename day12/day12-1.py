from collections import defaultdict
from os import path
from typing import List, Set, Tuple

#file_to_use = 'day12/day12-sample.txt'
file_to_use = 'day12/day12-input.txt'

graph = defaultdict(set)
paths = set()

def can_grow(path, g) -> bool:
    if path[-1] == 'end':
        return False
    else:
        for neightbor in g[path[-1]]:
            if neightbor[0].isupper():
                return True
            elif neightbor not in path:
                return True
        return False

def grow_paths(path, g) -> Set[Tuple[str]]:
    new_paths = set()
    for neighbor in g[path[-1]]:
        if neighbor[0].isupper():
            new_paths.add(path + (neighbor,))
        elif neighbor not in path:
            new_paths.add(path + (neighbor,))
    return new_paths


with open(file_to_use) as f:
    for line in [l.strip() for l in f]:
        a,b = line.split('-')
        graph[a].add(b)
        graph[b].add(a)

new_paths = set()
new_paths.add(('start',))

while len(new_paths) > 0:
    paths = paths.union(new_paths)
    new_paths = set()
    for p in frozenset(paths):
        if p[-1] != 'end':
            if can_grow(p, graph):
                new_paths = new_paths.union(grow_paths(p, graph))
                paths.remove(p)
            else:
                # I guess we just skip these dead-end ones for now
                pass

good_path_count = len({x for x in paths if x[-1] == 'end'})
print(f'There are {good_path_count} paths through the graph defined at {file_to_use}')



