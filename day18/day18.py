from collections import namedtuple
from itertools import permutations
from copy import deepcopy

def is_regular_number(pfn):
    return type(pfn) == int

def is_terminal_pair(pfn):
    return True if is_regular_number(pfn.left) and is_regular_number(pfn.right) else False

# char iterator or parent/left/right?
class SnailfishNum:
    def __init__(self, *args) -> None:
        if len(args) == 1:
            self.parent = None
            self.left = None
            self.right = None
            # Let's do some string parsing!
            stringerator = args[0]
            c = next(stringerator)

            # if the first char is a [ then we recurse for our left
            if c == '[':
                self.left = SnailfishNum(stringerator)
                self.left.parent = self
            else:
                # if the first char is a number, then we make left a regular number
                self.left =int(c)

            c = next(stringerator)
            # close braces don't do much
            while c == ']':
                c = next(stringerator)
                if c == '\n':
                    return
            if c == ',':
                # if comma, now we set the right
                c = next(stringerator)
                if c == '[':
                    self.right = SnailfishNum(stringerator)
                    self.right.parent = self
                else:
                    self.right = int(c)
            else:
                print('that should not be there')

        else: 
            self.parent = args[0]
            self.left = args[1]
            if len(args) == 3:
                self.right = args[2]
            else:
                self.right = None
    
    def to_string(self):
        if is_terminal_pair(self):
            return f'[{self.left},{self.right}]'
        s = f'[{self.left if is_regular_number(self.left) else self.left.to_string()},'
        if self.right == None:
            s += ']'
        else:
            s += f'{self.right if is_regular_number(self.right) else self.right.to_string()}]'
        return s

    def replace_child(self, old, new):
        if not is_regular_number(new):
            new.parent = self
        if self.left == old:
            self.left = new
        elif self.right == old:
            self.right = new
        else:
            print('no replacing today')

    def magnitude(self):
        mag_left, mag_right = 0, 0
        if is_regular_number(self.left): 
            mag_left = self.left
        elif is_terminal_pair(self.left):
            mag_left = (self.left.left * 3) + (self.left.right *2)
        else:
            mag_left = self.left.magnitude()
        
        if is_regular_number(self.right): 
            mag_right = self.right
        elif is_terminal_pair(self.right):
            mag_right = (self.right.left * 3) + (self.right.right *2)
        else:
            mag_right = self.right.magnitude()
        
        return (mag_left * 3) + (mag_right * 2)

    def add(self, sfn):
        if self.parent != None or sfn.parent != None:
            print('can''t add those two')
            return None
        
        new_sfn = SnailfishNum(None, self, sfn)
        self.parent, sfn.parent = new_sfn, new_sfn

        def find_explosion_candidate(sfn, depth=1):
            if sfn == None or is_regular_number(sfn):
                return None
            if depth > 4 and is_terminal_pair(sfn):
                return sfn

            left_candidate = find_explosion_candidate(sfn.left, depth + 1)
            if left_candidate != None:
                return left_candidate
            else:
                return find_explosion_candidate(sfn.right, depth + 1)

        def explode_pair(p):
            def find_and_add_to_left_neighbor(p, bonus):
                if p == None or p.parent == None: # if we're at the top, that's it
                    pass
                elif p.parent.right == p: # if we're the right branch, find the rightmost of the left branch
                    if is_regular_number(p.parent.left):
                        p.parent.left += bonus
                    else:
                        rightmost_from_root_add(p.parent.left, bonus)
                else: # if we're the left branch, go up until we are the right branch and then take the rightmost of the left
                    find_and_add_to_left_neighbor(p.parent, bonus)

            def find_and_add_to_right_neighbor(p, bonus):
                if p == None or p.parent == None: # if we're at the top, that's it
                    pass
                elif p.parent.left == p: # if we're the left branch, find the leftmost of the right branch
                    if p.parent.right != None: 
                        if is_regular_number(p.parent.right):
                            p.parent.right += bonus
                        else:
                            leftmost_from_root_add(p.parent.right, bonus)
                    else:
                        find_and_add_to_right_neighbor(p.parent, bonus)
                else: # if we're the right branch, go up until we're the left branch and take the leftmost of the right
                    find_and_add_to_right_neighbor(p.parent, bonus)

            def rightmost_from_root_add(p, bonus):
                if p.right == None:
                    rightmost_from_root_add(p.left, bonus)
                elif is_regular_number(p.right):
                    p.right += bonus
                elif is_terminal_pair(p.right):
                    p.right.right += bonus
                else:
                    rightmost_from_root_add(p.right, bonus)

            def leftmost_from_root_add(p, bonus):
                if is_regular_number(p.left):
                    p.left += bonus
                elif is_terminal_pair(p.left):
                    p.left.left += bonus
                elif p.left != None:
                    leftmost_from_root_add(p.left, bonus)

            #print(f'Exploding {p.to_string()}')

            if is_regular_number(p.parent.left):
                p.parent.left += p.left
            else:
                find_and_add_to_left_neighbor(p, p.left)
            
            if is_regular_number(p.parent.right):
                p.parent.right += p.right
            else:
                find_and_add_to_right_neighbor(p, p.right)
            p.parent.replace_child(p, 0)

        def find_and_split(sfn):
            def split_left(p):
                #print(f'Splitting left {p.to_string()}')
                new_left = p.left // 2
                new_right = p.left - new_left
                p.left = SnailfishNum(p, new_left, new_right)

            def split_right(p):
                #print(f'Splitting right {p.to_string()}')
                new_left = p.right // 2
                new_right = p.right - new_left
                p.right = SnailfishNum(p, new_left, new_right)
            
            if sfn == None:
                return False
            elif is_regular_number(sfn.left):
                if sfn.left >= 10:
                    split_left(sfn)
                    return True
            elif is_terminal_pair(sfn.left):
                if sfn.left.left >= 10:
                    split_left(sfn.left)
                    return True
                elif sfn.left.right >= 10:
                    split_right(sfn.left)
                    return True
            elif find_and_split(sfn.left):
                return True

            if is_regular_number(sfn.right):
                if sfn.right >= 10:
                    split_right(sfn)
                    return True
                else:
                    return False
            elif is_terminal_pair(sfn.right):
                if sfn.right.left >= 10:
                    split_left(sfn.right)
                    return True
                elif sfn.right.right >= 10:
                    split_right(sfn.right)
                    return True
                else:
                    return False
            else:
                return find_and_split(sfn.right)
                    
        # loop until no explosions or splits 
        did_explode, did_split = True, True
        while did_explode or did_split:
            did_explode = False
            to_explode = find_explosion_candidate(new_sfn)
            while to_explode != None:
                explode_pair(to_explode)
                # print(f'After explode: {new_sfn.to_string()}')
                did_explode = True
                to_explode = find_explosion_candidate(new_sfn)
            did_split = False
            did_split = find_and_split(new_sfn)
            #if did_split:
                # print(f'after split: {new_sfn.to_string()}')
        return new_sfn


file_to_read = 'day18/day18-input.txt'
#file_to_read = 'day18/day18-sample.txt'
current_sum = None

# sfn = SnailfishNum(iter('[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]\n'))
# print(sfn.to_string())
# print(sfn.magnitude())

# day18-1
# with open(file_to_read) as f:
#     # grab the first one
#     current_line = f.readline().rstrip()[1:]
#     current_sum = SnailfishNum(iter(current_line))
#     for l in f.readlines():
#         print(f'current total: {current_sum.to_string()}')
#         new_sfn = SnailfishNum(iter(l.rstrip()[1:]))
#         print(f'adding {new_sfn.to_string()}')
#         current_sum = current_sum.add(new_sfn)

#     print(f'Final sum from {file_to_read} is {current_sum.magnitude()}')

# day 18-2
sf_nums = []
max_magnitude = 0
with open(file_to_read) as f:
    for l in f.readlines():
        sf_nums.append(SnailfishNum(iter(l.rstrip()[1:])))

for a,b in permutations(range(len(sf_nums)), 2):
    a_copy = deepcopy(sf_nums[a])
    b_copy = deepcopy(sf_nums[b])
    new_sfn = a_copy.add(b_copy)
    new_mag = new_sfn.magnitude()
    if new_mag > max_magnitude:
        max_magnitude = new_mag

print(f'Max magnitude is {max_magnitude}')
    
