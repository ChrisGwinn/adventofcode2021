import re

file_to_use = 'day6/day6-input.txt'
#file_to_use = 'day6/day6-input-sample.txt'
DAYS_TO_SIMULATE = 256

fish_timer_histogram = [0 for i in range(10)]

with open(file_to_use) as f:
    for fish in re.split(r'\D+', f.readline().rstrip()):
        fish_timer_histogram[int(fish)] += 1

print(f'start with {sum(fish_timer_histogram)} fish')

for i in range(DAYS_TO_SIMULATE):
    fish_idx_hatch = i % 10
    fish_idx_restart = (fish_idx_hatch + 7) % 10
    fish_idx_new = (fish_idx_hatch + 9) % 10
    fish_timer_histogram[fish_idx_new] = fish_timer_histogram[fish_idx_hatch]
    fish_timer_histogram[fish_idx_restart] += fish_timer_histogram[fish_idx_hatch]
    fish_timer_histogram[fish_idx_hatch] = 0
    print(f'After {i + 1} days there are {sum(fish_timer_histogram)} fish')
