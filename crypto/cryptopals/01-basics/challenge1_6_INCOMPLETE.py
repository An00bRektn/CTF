#!/usr/bin/env python3
from base64 import b64decode

def xor(pt, key):
    b1, b2 = bytes.fromhex(pt), bytes.fromhex(key)
    return bytes([b1[i]^b2[i%len(b2)] for i in range(len(b1))])

def hamming_distance(str1, str2):
    binary_xored = "".join(format(c, 'b') for c in xor(str1.encode('latin-1').hex(), str2.encode('latin-1').hex()))
    return sum([int(b) for b in binary_xored])

if __name__ == "__main__":
    # Tests
    assert hamming_distance('this is a test', 'wokka wokka!!!') == 37

    # Actual Stuff
    with open('./input-files/6.txt', 'r') as f:
        ct = b64decode(f.read().replace('\n', ''))
    
    for keysize in range(2, 40):
        pass
    