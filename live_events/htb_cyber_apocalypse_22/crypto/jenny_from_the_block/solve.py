#!/usr/bin/python3
from pwn import *
from hashlib import sha256

BLOCK_SIZE = 32

def decrypt_block(block, secret):
    dec_block = b''
    for i in range(BLOCK_SIZE):
        val = (block[i]-secret[i]) % 256
        dec_block += bytes([val])
    return dec_block

r = remote('157.245.40.139',30855)
message = b'Command executed: cat secret.txt'

r.sendlineafter('>', 'cat secret.txt')
ct = r.recvlineS().strip()
blocks = [ct[i:i+64] for i in range(0, len(ct), 64)]

ref = bytes.fromhex(blocks[0])
init_key = b''
p = log.progress('brute forcing initial key...')
for i in range(BLOCK_SIZE):
    for guess in range(256):
        val = (message[i]+guess) % 256
        p.status(f'val: {val}\nref: {ref[i]}\nrec: {init_key}')
        if val == ref[i]:  
            init_key += bytes([guess])

info(f'init_key: {init_key.hex()}')
h = init_key
plaintext = b''
for block in blocks:
    block = bytes.fromhex(block)
    dec_block = decrypt_block(block, h)
    h = sha256(block + dec_block).digest()
    plaintext += dec_block

success(plaintext.decode('utf-8'))
