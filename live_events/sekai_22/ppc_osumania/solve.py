#!/usr/bin/env python3
import sys

beatmap = [l for l in sys.stdin][1:]
counter = 0

hold_state = [False, False, False, False]
for line in beatmap:
    beats = line[1:-2]
    for b in range(len(beats)):
        if beats[b] == '-':
            if hold_state[b] == False:
                counter += 1
            if hold_state[b] == True:
                hold_state[b] = False
        
        if beats[b] == '#':
            if hold_state[b] == False:
                hold_state[b] = True
            else:
                pass
        
print(counter)