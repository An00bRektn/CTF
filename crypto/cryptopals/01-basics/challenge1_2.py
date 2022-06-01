#!/usr/bin/env python3

def xor(hex1: str, hex2: str):
    b1, b2 = bytes.fromhex(hex1), bytes.fromhex(hex2)
    return bytes([a^b for a,b in zip(b1, b2)])

if __name__ == '__main__':
    h1 = '1c0111001f010100061a024b53535009181c'
    h2 = '686974207468652062756c6c277320657965'
    assert xor(h1, h2).hex() == '746865206b696420646f6e277420706c6179'
    print('Good!')