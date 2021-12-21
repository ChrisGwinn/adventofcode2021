from collections import defaultdict, namedtuple

file_to_read = 'day20/day20-input.txt'
#file_to_read = 'day20/day20-sample.txt'

enhancements = list()
# consider the infinite void
input_image = defaultdict(lambda:0)
Point = namedtuple('Point', 'x y')
image_size = 0

with open(file_to_read) as f:
    enhancements = [1 if c == '#' else 0 for c in  list(f.readline().rstrip())]
    f.readline()
    for line in [l.strip() for l in f]:
        x = 0
        for c in line:
            input_image[Point(x,image_size)] = 1 if c == '#' else 0
            x += 1
        image_size += 1

def pixel_to_int(image, p):
    ul = image[Point(p.x - 1, p.y - 1)]
    u = image[Point(p.x, p.y - 1)]
    ur = image[Point(p.x + 1, p.y - 1)]
    l = image[Point(p.x - 1, p.y)]
    c = image[p]
    r = image[Point(p.x + 1, p.y)]
    dl = image[Point(p.x -1, p.y + 1)]
    d = image[Point(p.x, p.y + 1)]
    dr = image[Point(p.x + 1, p.y + 1)]

    idx = (((((((((((((((ul << 1) + u) << 1) + ur) << 1) + l) << 1) + c) << 1) + r) << 1) + dl) << 1) + d) << 1) + dr
    return enhancements[idx]

steps = 50

for _ in range(steps):
    if input_image['void'] == 1:
        new_image = defaultdict(lambda:enhancements[511])
    else:
        new_image = defaultdict(lambda:enhancements[0])
    
    for y in range(-1, image_size + 1):
        #l = '#' if infinite_void == 1 else '.'
        for x in range(-1, image_size + 1):
            #l +='#' if pixel_to_int(input_image, Point(x,y)) == 1 else '.'
            new_image[Point(x + 1, y + 1)] = pixel_to_int(input_image, Point(x,y))
        #l += '#' if infinite_void == 1 else '.'
        #print(l)
    input_image = new_image
    image_size += 2
    #print('=======================')

print(f'After {steps} there are {len(list(filter(lambda x: x == 1, input_image.values())))} pixels lit')