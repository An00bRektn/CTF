#!/usr/bin/env python3
#import pprint

def chunks(n, l):
    return [l[i:i+n] for i in range(0, len(l), n)]

a = [-43, 61, 58, 5, -4, -11, 64, -40, -43, 61, 62, -51, 46, 15, -49, -44, 47, 4, 6, -7, 47, 7, -59, 52, -15, 11, 7, 61, 0]
b = [6, 106, 10, 0, 119, 52, 51, 101, 0, 0, 15, 48, 116, 22, 10, 58, 125, 100, 102, 33]
c = [304, 357, 303, 320, 304, 307, 349, 305, 257, 337, 340, 309, 428, 270, 66]
d = [52, 52, 95, 95, 110, 49, 51, 51, 95, 110, 110, 53]

flag = [0 for _ in range(58)]

for i,di in enumerate(d):
    index = i*5
    flag[index] = di

# Guessing based off of what characters were left after the initial passes
flag[7] = ord('_')
flag[13] = ord('5')
flag[16] = ord('4')
flag[18] = ord('m')
flag[22] = ord('1')
flag[29] = ord('h')
flag[37] = ord('0')
flag[42] = ord('f')
flag[46] = ord('d')
flag[49] = ord('u')
flag[52] = ord('7')

for i,ai in enumerate(a):
    index = i*2
    if flag[index] != 0 and flag[index+1] == 0:
        flag[index+1] = flag[index] - ai
    elif flag[index+1] != 0 and flag[index] == 0:
        flag[index] = ai + flag[index+1]
    
two = chunks(3, flag)
for i,bi in enumerate(b):
    index = i*3
    try:
        if two[i].count(0) < 2 and two[i].count(0) != 0:
            nulli = two[i].index(0)
            two[i].remove(0)
            flag[index+nulli] = two[i][0] ^ two[i][1] ^ bi
    except IndexError:
        pass


for i,ai in enumerate(a):
    index = i*2
    if flag[index] != 0 and flag[index+1] == 0:
        flag[index+1] = flag[index] - ai
    elif flag[index+1] != 0 and flag[index] == 0:
        flag[index] = ai + flag[index+1]

three = chunks(4, flag)
for i,ci in enumerate(c):
    index = i*4
    try:
        if three[i].count(0) < 2 and three[i].count(0) != 0:
            nulli = three[i].index(0)
            three[i].remove(0)
            flag[index+nulli] = ci - three[i][0] - three[i][1] - three[i][2]
    except IndexError:
        pass


print(bytearray(flag))
#pprint.pprint(chunks(4, bytearray(flag).decode()))
