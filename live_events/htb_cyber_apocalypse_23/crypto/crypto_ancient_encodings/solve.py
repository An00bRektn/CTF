#!/usr/bin/env python3
from Crypto.Util.number import long_to_bytes
from base64 import b64decode

with open("output.txt", "r") as fd:
    enc = int(fd.read(), 16)

dec = b64decode(long_to_bytes(enc))
print(f"[+] FLAG: {dec}")
