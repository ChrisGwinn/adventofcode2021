from collections import namedtuple

Beacon = namedtuple('Beacon', 'x y z')

#file_to_read = 'day19/day19-input.txt'
file_to_read = 'day19/day19-sample.txt'

scanners = []
active_scanner = None

with open(file_to_read) as f:
    for l in f.readlines():
        if l[:3] == '---':
            active_scanner = set()
            scanners += active_scanner
        elif l[0] == '\n':
            active_scanner = None
        else:
            x,y,z = l.rstrip().split(',')
            active_scanner.add(Beacon(x,y,z))

# In total, each scanner could be in any of 24 different orientations: 
# facing positive or negative x, y, or z, and considering any of four directions "up" from that facing.
# TODO: I don't understand why this is 24 permutations

# It feels like matrix math is what we want here? But maybe not.


