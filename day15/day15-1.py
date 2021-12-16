from collections import defaultdict, namedtuple
from math import dist, inf

#file_to_use = 'day15/day15-sample.txt'
file_to_use = 'day15/day15-input.txt'

# OK, treating this as a grid is going to be a mess, so 
# let's start by thinking about this as a graph with useful labels

graph = defaultdict() # point tuple to set of (point, weight) tuples
Point = namedtuple('Point', 'x y')
start, end = Point(0,0), None

with open(file_to_use) as f:
    point_risks = dict() # I don't want to store these in the graph
    x,y = 0,0

    line = f.readline().strip()
    while line != '':
        x = 0
        for risk in line:
            p = Point(x,y)
            point_risks[p] = int(risk)
            graph[p] = set()

            u = Point(p.x, p.y - 1) 
            if u in graph:
                graph[u].add((p, point_risks[p]))
                graph[p].add((u, point_risks[u]))

            l = Point(p.x - 1, p.y) 
            if l in graph:
                graph[l].add((p, point_risks[p]))
                graph[p].add((l, point_risks[l]))
            # the other ones won't be loaded yet
            x += 1 
        line = f.readline().strip()
        y += 1
    end = Point(x - 1, y - 1)

current = start
current_distance = 0
unvisited = {p: inf for p in graph.keys()} # TODO: consider a priority queue or buckets
visited = {}

while current not in visited:
    for neighbor, distance in graph[current]:
        if neighbor in unvisited:
            new_distance = current_distance + distance
            if unvisited[neighbor] > new_distance:
                unvisited[neighbor] = new_distance
    visited[current] = current_distance
    del unvisited[current]
    if unvisited:
        current = min(unvisited, key=unvisited.get)
        current_distance = unvisited[current]

print(visited[end])
