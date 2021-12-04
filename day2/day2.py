
depth = 0
distance = 1
aim = 2
sub_loc = [0,0,0]

def forward(sub_loc, amount):
    sub_loc[distance] += amount
    sub_loc[depth] += sub_loc[aim] * amount

def down(sub_loc, amount):
    sub_loc[aim] += amount

with open('day2-input.txt') as f:
    for line in f:
        direction, amount = line.split()
        if direction == 'forward':
            forward(sub_loc, int(amount))
        elif direction == 'down':
            down(sub_loc, int(amount))
        elif direction == 'up':
            down(sub_loc, -int(amount))

print(sub_loc)
print(sub_loc[distance] * sub_loc[depth])