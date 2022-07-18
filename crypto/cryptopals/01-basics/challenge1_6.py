#!/usr/bin/env python3
from base64 import b64decode
from challenge1_4 import *
from itertools import combinations

"""
    This is the result of the avalanche that is lazy coding
    Lessons learned:
        1. Only operate on bytes, use strings for pretty printing
        2. Write better function protypes
        3. Stop doing the sort-by-keys one liner I found on stack overflow
        4. If one part of your analysis is lazy, the other needs to be more invovled to compensate
        5. Just code it better
"""

def xor(pt, key):
    b1, b2 = bytes.fromhex(pt), bytes.fromhex(key)
    return bytes([b1[i]^b2[i%len(b2)] for i in range(len(b1))])

def hamming_distance(str1:str, str2:str):
    binary_xored = "".join(format(c, 'b') for c in xor(str1.encode('latin-1').hex(), str2.encode('latin-1').hex()))
    return sum([int(b) for b in binary_xored])

if __name__ == "__main__":
    # Tests
    assert hamming_distance('this is a test', 'wokka wokka!!!') == 37

    # Actual Stuff
    with open('./input-files/6.txt', 'r') as f:
        ct = b64decode(f.read().replace('\n', ''))

    # find key size
    # Because my frequency analysis was so primitive, they way we find potential
    # length candidates has to be a little more complex
    sizes = {}
    for l in range(2, 41):
        chunks = [ct[i:i + l] for i in range(0, len(ct), l)][:4]
        combs = combinations(chunks, 2)
        dist = 0
        for c1, c2 in combs:
            dist += hamming_distance(c1.decode('latin-1'), c2.decode('latin-1'))
        
        dist /= 6*l
        sizes[l] = dist

    print(sizes)
    key_vals = list(dict(sorted(sizes.items(), key=lambda item: item[1])))[0:3]
    keys = []
    print(f"[+] KEY VALS: {key_vals}")
    for key_len in key_vals:
        cts = [ct[i:i+key_len] for i in range(0, len(ct), key_len)]

        transpose_blocks = []
        for i in range(key_len):
            block = b""
            for enc in cts:
                try:
                    block += bytes([enc[i]])
                except:
                    pass
            transpose_blocks.append(block)

        key = b''
        for block in transpose_blocks:
            scored = {}
            for i in range(257):
                decrypted = "".join([chr(c^i) for c in block])
                score = naive_freq_analysis(decrypted.upper())
                if score != -1:
                    scored[i] = score

            key += bytes([list(dict(sorted(scored.items(), key=lambda item: item[1])))[0]])

        keys.append(bytes(key))

    print("-"*10 + "POSSIBLE" + "-"*10)
    for k in keys:
        print(f"Key: {k.hex()}")
        print(f"XOR: {xor(ct.hex(), k.hex())}")
