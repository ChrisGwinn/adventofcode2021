from functools import reduce
from os import get_inheritable
from operator import mul

#file_to_use = 'day9/day9-sample.txt'
file_to_use = 'day9/day9-input.txt'

class Location:
    def __init__(self, x, y, height) -> None:
        self.x = x
        self.y = y
        self.height = height
        self.risk_level = height + 1
        self.meets_criteria = True
        self.basin = None

grid = None

with open(file_to_use) as f:
    y = 0
    for line in [l.strip() for l in f]:
        if grid == None:
            grid = [[] for i in range(len(line))]
        for x in range(len(line)):
            grid[x].append(Location(x, y, int(line[x])))
        y += 1
        
# spin through points by column, skipping ones that are marked bad
# does marking them bad count as modifying the collection?
for column in grid:
    # is the next one lower? 
#   yes? : mark this one as bad
#   no?  : mark the next one as bad
    for y in range(len(column) - 1):
        if column[y].height < column[y+1].height:
            column[y+1].meets_criteria = False
        elif column[y].height > column[y+1].height:
            column[y].meets_criteria = False
        else:
            column[y+1].meets_criteria = False
            column[y].meets_criteria = False

# do the same by row
for y in range(len(grid[0])):
    for x in range(len(grid) - 1):
        if grid[x][y].height < grid[x+1][y].height:
            grid[x+1][y].meets_criteria = False
        elif grid[x][y].height > grid[x+1][y].height:
            grid[x][y].meets_criteria = False
        else:
            grid[x+1][y].meets_criteria = False
            grid[x][y].meets_criteria = False

answer_9_1 = 0
basin_count = 0
basin_sizes = {}

def expand_basin_from_loc(loc):
    # up?
    loc_to_check = []
    if loc.y > 0:
        loc_to_check.append(grid[loc.x][loc.y - 1])
    # down?
    if loc.y < len(grid[0]) - 1:
        loc_to_check.append(grid[loc.x][loc.y + 1])
    # left?
    if loc.x > 0:
        loc_to_check.append(grid[loc.x - 1][loc.y])
    # right?
    if loc.x < len(grid) - 1:
        loc_to_check.append(grid[loc.x + 1][loc.y])

    for l in loc_to_check:
        if l.basin == None and loc.height <= l.height and l.height != 9:
            l.basin = loc.basin
            basin_sizes[loc.basin] += 1
            expand_basin_from_loc(l)

for col in grid:
    for low_point in filter(lambda x: x.meets_criteria, col):
        low_point.basin = basin_count
        basin_sizes[basin_count] = 1
        expand_basin_from_loc(low_point)
        basin_count += 1
        answer_9_1 += low_point.risk_level

print(f'9-1 answer {answer_9_1}')
print(f'9-2 answer {reduce(mul, sorted([i[1] for i in basin_sizes.items()], reverse=True)[:3], 1)}')