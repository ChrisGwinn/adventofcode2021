from collections import namedtuple
from typing import Iterator
import re

Target = namedtuple('Target', 'min_x max_x min_y max_y')
Point = namedtuple('Point', 'x y')
Velocity = namedtuple('Velocity', 'x y')

def point_in_target(p: Point,t: Target) -> bool:
    if t.min_x <= p.x <= t.max_x:
        return True if t.min_y <= p.y <= t.max_y else False
    else:
        return False

def points_from_shot(v: Velocity) -> Iterator[Point]:
    current_velocity = v
    current_loc = Point(0,0) 
    while True:
        current_loc = Point(current_loc.x + current_velocity.x, current_loc.y + current_velocity.y)
        if current_velocity.x > 0:
            current_velocity = Velocity(current_velocity.x - 1, current_velocity.y -1)
        elif current_velocity.x < 0:
            current_velocity = Velocity(current_velocity.x + 1, current_velocity.y -1)
        else:
            current_velocity = Velocity(0, current_velocity.y -1)
        yield current_loc

# Maybe not a good idea, but we're assuming they're shooting right and down
# Adding original velocity would help here
def missed_it(p: Point,t: Target) -> bool:
    return True if t.max_x < p.x or p.y < t.min_y else False

# testing
#target = Target(20,30,-10,-5)
#target area: x=257..286, y=-101..-57
target = Target(257, 286, -101, -57)

# again, assuming right-firing
max_initial_x = target.max_x + 1 # can't go higher than this or it'll immediately miss
min_initial_x = 20 # TODO: surely there is math for x + x-1 +...
max_initial_y = 250 # TODO: this is the one I don't know, and we may need to find it by binary search
min_initial_y = target.min_y - 1

highest_y_for_hit = 0
all_hits = set()

# TODO: there's probably some sort of newton's method like approach that's more efficient than exploring the entire space
# and tweaking start variables
for x in range(min_initial_x, max_initial_x):
    for y in range(min_initial_y, max_initial_y):
        velocity = Velocity(x,y)
        highest_y_for_shot = 0
        for p in points_from_shot(velocity):
            if p.y > highest_y_for_shot:
                highest_y_for_shot = p.y
            if point_in_target(p, target):
                print(f'Hit! with {velocity}. Hightest Y was {highest_y_for_shot}')
                print(p)
                if highest_y_for_shot > highest_y_for_hit:
                    highest_y_for_hit = highest_y_for_shot
                all_hits.add(velocity)
                break
            if missed_it(p, target):
                #print(f'Missed! with {velocity}')
                #print(p)
                break

print(f'Highest from all shots: {highest_y_for_hit}')
print(f'All hits= {len(all_hits)}')
