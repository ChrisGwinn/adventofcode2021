# As the submarine drops below the surface of the ocean, it automatically performs a sonar sweep of the nearby sea floor. On a small screen, the sonar sweep report (your puzzle input) appears: each line is a measurement of the sea floor depth as the sweep looks further and further away from the submarine.

# For example, suppose you had the following report:

# 199
# 200
# 208
# 210
# 200
# 207
# 240
# 269
# 260
# 263
# This report indicates that, scanning outward from the submarine, the sonar sweep found depths of 199, 200, 208, 210, and so on.

# The first order of business is to figure out how quickly the depth increases, just so you know what you're dealing with - you never know if the keys will get carried into deeper water by an ocean current or a fish or something.

# To do this, count the number of times a depth measurement increases from the previous measurement. (There is no measurement before the first measurement.) In the example above, the changes are as follows:

# 199 (N/A - no previous measurement)
# 200 (increased)
# 208 (increased)
# 210 (increased)
# 200 (decreased)
# 207 (increased)
# 240 (increased)
# 269 (increased)
# 260 (decreased)
# 263 (increased)
# In this example, there are 7 measurements that are larger than the previous measurement.

from os import write

# Turn into an array?
windows = [None,None,None,None]
signal_count = 0
window_length = 3
last_closed_window_total = None

with open('day1-input.txt') as f:
    total_window_increases = 0
    for line in f:
        signal = int(line)

        wid = signal_count % (4)

        if wid == 0:
            # open window 0
            windows[0] = signal
            # close window 2
            if windows[2] != None:
                windows[2] += signal
                if (last_closed_window_total != None) and (windows[2] > last_closed_window_total):
                    total_window_increases += 1
                if last_closed_window_total != None:
                    last_closed_window_total = windows[2]
                
                windows[2] = None
             # increment window 3
            if windows[3] != None:
                windows[3] += signal
        elif wid == 1:
            # open window 1
            windows[1] = signal
            # close window 3
            if windows[3] != None:
                windows[3] += signal
                if (last_closed_window_total != None) and (windows[3] > last_closed_window_total):
                    total_window_increases += 1
                last_closed_window_total = windows[3]
                windows[3] = None
            # increment window 0
            if windows[0] != None:
                windows[0] += signal
        elif wid == 2:
            # open window 2
            windows[2] = signal
            # close window 0
            if windows[0] != None:
                windows[0] += signal
                if (last_closed_window_total != None) and (windows[0] > last_closed_window_total):
                    total_window_increases += 1
                last_closed_window_total = windows[0]
                windows[0] = None
            # increment window 1
            if windows[1] != None:
                windows[1] += signal
        else:
            # open window 3
            windows[3] = signal
            # close window 1
            if windows[1] != None:
                windows[1] += signal
                if (last_closed_window_total != None) and (windows[1] > last_closed_window_total):
                    total_window_increases += 1
                last_closed_window_total = windows[1]
                windows[1] = None
            # increment window 2
            if windows[2] != None:
                windows[2] += signal
        
        signal_count += 1
        #TODO: parameterize this stupid logic
        #TODO: consider doing the first window outside the main logic to skip all the dumb checks.
        #TODO: optional trickiness - do this w/o a separate variable by using the list value

    print(total_window_increases)


    # Problem 1 solution
    #     current = int(line)
    #     if prev != None and current > prev:
    #         count += 1
    #     prev = current

    # print(count)