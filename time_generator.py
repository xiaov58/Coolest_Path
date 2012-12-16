
import random
import sys

cnt = 10
final = [[]]

for k in range(10):
    on = []
    off = []
    time = 0
    result = []
    store = 0
    for i in range(cnt):
        on.append(random.expovariate(float(sys.argv[1])))
        
    for i in range(cnt):
        off.append(random.expovariate(float(sys.argv[2])))
        
    for i in range(cnt):
        if store < 50:
            time += off[i]
            start = time
            time += on[i]
            end = time
            result.append([start, end])
            store = end
    
    final.append([result])

print final
    
    
    
    
