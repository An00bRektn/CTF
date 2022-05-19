#!/usr/bin/env python3
# Adapted from: https://github.com/jvdsn/crypto-attacks/blob/master/attacks/rc4/fms.py
from pwn import *
import json
from collections import Counter

def possible_key_bit(key, c):
    s = [i for i in range(256)]
    j = 0
    for i in range(len(key)):
        j = (j + s[i] + key[i]) % 256
        tmp = s[i]
        s[i] = s[j]
        s[j] = tmp

    return (c[0] - j - s[len(key)]) % 256

context.log_level = 'info'

r = remote('178.62.73.26', 31267)

def oracle(iv, pt):
    msg = '{"option":"encrypt", "iv":"'+ iv.hex() +'", "pt":"'+ pt.hex() +'"}'
    r.sendlineafter('>', msg)
    return r.recvlineS().strip()

def validate(key):
    msg = '{"option":"claim", "key":"'+ key.hex() +'"}'
    r.sendlineafter('>', msg)
    return r.recvlineS().strip()

"""
Recovers the hidden part of an RC4 key using the Fluhrer-Mantin-Shamir attack.
:param encrypt_oracle: the padding oracle, returns the encryption of a plaintext under a hidden key concatenated with the iv
:param key_len: the length of the hidden part of the key
:return: the hidden part of the key
"""
p = log.progress("working...")
key = bytearray([3, 255, 0])
for a in range(27):
    key[0] = a + 3
    possible = Counter()
    for x in range(256):
        key[2] = x
        c = bytes.fromhex(json.loads(oracle(key[:3], b'\x00'))['ct'])
        p.status(f"\n  ct: {c.hex()}\n key: {key.hex()}")
        possible[possible_key_bit(key, c)] += 1
    key.append(possible.most_common(1)[0][0])


attempt = validate(key[3:])
info(f"attempt: {attempt}")