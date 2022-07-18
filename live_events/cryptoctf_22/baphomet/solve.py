#!/usr/bin/env python3
from base64 import b64decode

with open('flag.enc', 'rb') as filp:
    ct = filp.read()

# Known plaintext: CCTF{ -> Q0NURn -> q0nurN
known_pt = b'q0nurN'
key = b''
for i, b in enumerate(known_pt):
    key += bytes([ct[i] ^ b])

pt = b''
for i, c in enumerate(ct):
    pt += bytes([c ^ key[i%len(key)]])

# Crazy that python just has a swapcase function :o
print(b64decode(str.swapcase(pt.decode('utf-8'))))