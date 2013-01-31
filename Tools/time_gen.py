
#usage example: python time_gen.py 0.05 0.1

import random
import sys


# experiment time
experiment_time = 50
# hopefully length of 10 can generate longer than 50s which is the experiment time
# otherwise we need to increase this.
cnt = 15
# total channel number
channel_number = 20

final = []

for k in range(channel_number):
    on = []
    off = []
    timestamp = 0
    result = []
    for i in range(cnt):
        on.append(random.expovariate(float(sys.argv[1])))
        off.append(random.expovariate(float(sys.argv[2])))
        if timestamp + off[i] < experiment_time:
            timestamp += off[i]
            start = timestamp
            timestamp += on[i]
            end = timestamp
            result.append([start, end])
    
    final.append(result)

print final

    
    
    
    
