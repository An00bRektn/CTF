from os import urandom
from Crypto.Cipher import AES
import random

def pkcs7_pad(plaintext: bytes, block_size=16):
    space = block_size - (len(plaintext) % block_size)
    return plaintext + (space * bytes([space]))

def _gen_random_bytes():
    return urandom(random.randint(5,10))

def encrypt(pt, debug=False):
    key = urandom(16)
    pt = pkcs7_pad(_gen_random_bytes() + bytes.fromhex(pt) + _gen_random_bytes())

    mode = random.randint(1,2) # 1 for ECB, 2 for CBC

    if mode == 2:
        cipher = AES.new(key, mode, urandom(16))
        if debug:
            return cipher.encrypt(pt), mode
        else:
            return cipher.encrypt(pt)
    else:
        cipher = AES.new(key, mode)
        if debug:
            return cipher.encrypt(pt), mode
        else:
            return cipher.encrypt(pt)

def detect_ecb_cbc(ct, block_size = 16):
    blocks = [ct[i:i+block_size] for i in range(0, len(ct), block_size)]
    if len(blocks) != len(set(blocks)):
        return 1
    else:
        return 2
    
"""Success rate is pretty bad but it's probably because some of the lines aren't long enough"""
if __name__ == "__main__":
    # https://jeffsum.com
    with open('input-files/corpus.txt', 'r') as f:
        corpus = [line.strip().encode('latin-1') for line in f.read().split('\n')]

    wins = 0
    for line in corpus:
        ct, mode = encrypt(line.hex(), True)
        predict = detect_ecb_cbc(ct)
        if predict == mode:
            wins += 1
    
    print(f"[+] Success rate: {wins / len(corpus) * 100}")