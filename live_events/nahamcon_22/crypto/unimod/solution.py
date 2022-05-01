#!/usr/bin/env python3
# At the time of doing the CTF, I was too dumb to realize that the modulo barely mattered and 
# you could just find the original k by subtracting and apply that to the rest of the flag

flag = ''
ct = open('out', 'r').read().strip()
k = ord(ct[0]) - ord('f')
print(f"[+] k: {k}")

for c in ct:
    flag += chr((ord(c) - k))

print(f"[+] FLAG: {flag}")