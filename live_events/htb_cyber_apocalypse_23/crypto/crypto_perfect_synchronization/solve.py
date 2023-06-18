#!/usr/bin/env python3

valid_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ{}_ '

with open('output.txt', 'r') as fd:
    cts = [x.strip() for x in fd.readlines()]

seen = {}
sub = 0
temp = ""
for c in cts:
    if c in seen:
        seen[c][0] += 1
    else:
        seen[c] = [1, sub]
        sub += 1

    temp += valid_chars[seen[c][1]]

# quipquip should be able to figure out what the original message should be
print(temp)
print("Take the first 1000 or so characters and paste into quipquip")

# once you know what the message should be, go to dcode.fr and search
# monoalphabetic substitution cipher
solve_dict = dict(zip(valid_chars, "FREQUNCY ALSIBDOTHGVWMPKXZJ{_}"))
for t in temp:
    print(solve_dict[t], end="")
print("")
#print(almost_pt)