#!/usr/bin/env python3

def xor(pt, key):
    b1, b2 = bytes.fromhex(pt), bytes.fromhex(key)
    return bytes([b1[i]^b2[i%len(b2)] for i in range(len(b1))])

if __name__ == '__main__':
    pt = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
    ct = "0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f"
    key = 'ICE'
    assert xor(pt.encode('latin-1').hex(), key.encode('latin-1').hex()).hex() == ct
    print("Good!")
    