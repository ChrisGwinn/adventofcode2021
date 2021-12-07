import re

file_to_use = 'day7/day7-input.txt'

with open(file_to_use) as f:
    crabs = list(map(int, re.split(r'\D+', f.readline().rstrip())))
    crab_max_pos = max(crabs)
    fuel_to_pos_sums_7_1 = [0 for i in range(crab_max_pos + 1)]
    fuel_to_pos_sums_7_2 = [0 for i in range(crab_max_pos + 1)]
    for c in crabs:
        for i in range(crab_max_pos + 1):
            fuel_to_pos_sums_7_1[i] += abs(c - i)
            #forgive me for the repeated and inefficient math
            fuel_to_pos_sums_7_2[i] += sum(range(abs(c - i) + 1))
    print (f'7-1 solution: {min(fuel_to_pos_sums_7_1)}')
    print (f'7-2 solution: {min(fuel_to_pos_sums_7_2)}')
