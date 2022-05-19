#!/usr/bin/env python3
def deriveKey(key):
    derived_key = []

    for i, char in enumerate(key):
        previous_letters = key[:i]
        new_number = 1
        for j, previous_char in enumerate(previous_letters):
            if previous_char > char:
                derived_key[j] += 1
            else:
                new_number += 1
        derived_key.append(new_number)
    return derived_key

def transpose(array):
    return [row for row in map(list, zip(*array))]

def flatten(array):
    return "".join([i for sub in array for i in sub])

key = str(729513912306026)
derived_key = deriveKey(key)
print(derived_key)
width = len(key)
inv_derived_key = [11,13,5,8,2,9,14,6,10,4,12,15,1,3,7] # used dcode.fr

with open('encrypted_messages.txt', 'r') as f:
    cts = [x.strip() for x in f.readlines()]

for ct in cts:
    # Unflatten
    blocks = [ct[i:i+7] for i in range(0, len(ct), 7)]
    blocks = [list(b) for b in blocks]
    # Reverse the mixup
    pt = [blocks[inv_derived_key.index(i + 1)][::-1] for i in range(width)]

    # Un-transpose
    pt = transpose(pt)

    # flatten
    print(flatten(pt))

    


# Testing below - turns out the PRNG generates the same number every time
# so all you need to do is decrypt the columnar cipher with the same key
"""
import os
class PRNG:
    def __init__(self, seed):
        self.p = 0x2ea250216d705
        self.a = self.p
        self.b = int.from_bytes(os.urandom(16), 'big')
        self.rn = seed

    def next(self):
        self.rn = ((self.a * self.rn) + self.b) % self.p
        return self.rn

seed = int.from_bytes(os.urandom(16), 'big')
rng = PRNG(seed)

for i in range(10):
    print(f"[+] p = {rng.p}\n    a = {rng.a}\n    b = {rng.b}\n    n = {rng.rn}")
    print(f"  \\\\--> key = {str(rng.next())}")
"""
