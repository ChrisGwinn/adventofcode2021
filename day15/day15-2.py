from collections import defaultdict, namedtuple
from math import dist, inf
from heapq import heappop, heappush

#file_to_use = 'day15/day15-sample.txt'
file_to_use = 'day15/day15-input.txt'

# OK, treating this as a grid is going to be a mess, so 
# let's start by thinking about this as a graph with useful labels

graph = defaultdict() # point tuple to set of (point, weight) tuples
Point = namedtuple('Point', 'x y')
start, end = Point(0,0), None

with open(file_to_use) as f:
    file_lines = f.readlines()
    point_risks = dict() # I don't want to store these in the graph

    def risk_calculator(r, shifts):
        # It is past my bedtime and I couldn't get the math fast
        risks = [9,1,2,3,4,5,6,7,8]
        i = risks.index(r)
        return risks[(r + shifts) % 9]

    x,y = 0,0
    for y_repeast in range(5):
        for line in [l.strip() for l in file_lines]:
            x = 0
            for x_repeat in range(5):
                for risk in [int(r) for r in line]:
                    p = Point(x,y)
                    point_risks[p] = risk_calculator(risk, x_repeat + y_repeast)
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
            y += 1
    end = Point(x - 1, y - 1)

# part 2
# Option 1 - djikstra again, maybe with a priority queue or something so it doesn't choke
# option 2 - solve each grid separately? Map each edge node to every other edge node, then
# collapse the grid down into those nodes and solve again? 

queue = [(0, start)]
distances = defaultdict(lambda: float('inf'))
distances[start] = 0
visited = set()

while end not in visited:
    _, point = heappop(queue)
    if point not in visited:
        visited.add(point)
        dist = distances[point]
    
    for neighbor, neightbor_dist in graph[point]:
        if neighbor not in visited:
            new_dist = dist + neightbor_dist
            if new_dist < distances[neighbor]:
                heappush(queue, (new_dist, neighbor))
                distances[neighbor] = new_dist

print(distances[end])