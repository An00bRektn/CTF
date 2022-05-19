#!/usr/bin/env python3
# Reference: zachgrace.com/posts/attacking-ecb
# Note that this is, in the conventional definition of it, NOT a padding oracle attack
# but it has the spirit of one.
from pwn import *

r = remote('178.62.83.221', 31873)

def oracle(plaintext: str):
    r.sendlineafter(">", plaintext.encode('latin-1').hex())
    return r.recvlineS().strip()

flag = ""
p = log.progress(f'working...')
while True: 
    padding = 'B' * 4 +'A' * (31-len(flag))
    ref = oracle(padding)
    for c in range(33, 126):
        ct = oracle(padding+flag+chr(c))
        p.status(f"\n  ct: {ct[64:96]}\n ref: {ref[64:96]}\nflag: {flag}\n pad: {padding+flag+chr(c)}")
        if ct[64:96] == ref[64:96]:
            flag += chr(c)
            break
    if '{' in flag:
        break

success(flag)
