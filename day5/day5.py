from collections import namedtuple
import re

Point = namedtuple('Point', 'x y')
Segment = namedtuple('Segment', 'start end')
segments = []

def segment_to_points(seg):
    x_step, y_step, steps = 0,0, max(abs(seg.start.x - seg.end.x), abs(seg.start.y - seg.end.y))
    if seg.start.x == seg.end.x:
        y_step = 1 if seg.start.y < seg.end.y else -1
    elif seg.start.y == seg.end.y:
        x_step = 1 if seg.start.x < seg.end.x else -1
    else:
        x_step = 1 if seg.start.x < seg.end.x else -1
        y_step = 1 if seg.start.y < seg.end.y else -1
    
    return [Point(seg.start.x + (x_step * i), seg.start.y + (y_step * i)) for i in range(steps + 1)]

file_to_use = 'day5/day5-input.txt'
#file_to_use = 'day5/day5-sample.txt'

with open(file_to_use) as f:
    for line in f:
        match_result = re.split(r'\D+', line)
        s = Segment(Point(int(match_result[0]), int(match_result[1])), 
                    Point(int(match_result[2]), int(match_result[3])))
        segments.append(s)
        
point_cloud_3_1 = {}
# non-diagonal segments
for s in filter(lambda x: x.start.x == x.end.x or x.start.y == x.end.y, segments):
    #print(f'finding points for {s}')
    for p in segment_to_points(s):
        #print(f'found point{p}')
        if p in point_cloud_3_1:
            point_cloud_3_1[p] += 1
        else:
            point_cloud_3_1[p] = 1

overlapping_points_3_1 = list(filter(lambda x: x[1] > 1, point_cloud_3_1.items()))
print(f'3-1 answer: {len(overlapping_points_3_1)}')

# now that we don't need to filter out non-diagonal segments, this is easier
point_cloud_3_2 = {}
for s in segments:
    for p in segment_to_points(s):
        if p in point_cloud_3_2:
            point_cloud_3_2[p] +=1
        else:
            point_cloud_3_2[p] = 1

overlapping_points_3_2 = list(filter(lambda x: x[1] > 1, point_cloud_3_2.items()))
print(f'3-2 answer: {len(overlapping_points_3_2)}')
