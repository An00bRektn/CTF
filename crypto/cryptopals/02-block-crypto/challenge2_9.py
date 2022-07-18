#!/usr/bin/env python3

def pkcs7_pad(plaintext: bytes, block_size=16):
    space = block_size - (len(plaintext) % block_size)
    return plaintext + (space * bytes([space]))

if __name__ == "__main__":
    test = b'YELLOW SUBMARINE'
    assert pkcs7_pad(test, 20) == b'YELLOW SUBMARINE\x04\x04\x04\x04'
    print('Good!')

