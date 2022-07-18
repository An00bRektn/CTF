#!/usr/bin/env python3
from Crypto.Cipher import AES
from base64 import b64decode
"""
    Is using PyCryptodome kind of cheating here?
    I guess.
    Am I too lazy to take an AES implementation I made for something else and reuse it here?
    Yes.
"""

with open('input-files/10.txt', 'r') as f:
    ct = b64decode(f.read().replace('\n', '').strip())

key = b'YELLOW SUBMARINE'
iv = b'\x00' * 16
cipher = AES.new(key, AES.MODE_CBC, iv)
print(cipher.decrypt(ct))