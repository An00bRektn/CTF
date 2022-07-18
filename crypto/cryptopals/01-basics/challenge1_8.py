#!/usr/bin/env python3

with open('input-files/8.txt') as f:
    cts = [line.strip() for line in f.readlines()]

for ct in cts:
    blocks = [ct[i:i+32] for i in range(0, len(ct), 32)]
    if len(blocks) != len(set(blocks)):
        print(f"[+] ECB? {ct}")