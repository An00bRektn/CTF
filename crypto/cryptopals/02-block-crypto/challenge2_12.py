from os import urandom
from Crypto.Cipher import AES
from base64 import b64decode
from pwn import *       # For pretty logging :)

def pkcs7_pad(plaintext: bytes, block_size=16):
    space = block_size - (len(plaintext) % block_size)
    return plaintext + (space * bytes([space]))

KEY = urandom(16)
SECRET = b64decode('Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK')

def encrypt(pt):
    pt = pkcs7_pad(bytes.fromhex(pt) + SECRET)
    cipher = AES.new(KEY, AES.MODE_ECB)
    return cipher.encrypt(pt)

def determine_block_size():
    block_size = 1
    ct_ref = encrypt((b'A' * block_size).hex())
    changed = 0
    while True:
        new_ct = encrypt((b'A' * (block_size + 1)).hex())
        if len(new_ct) != len(ct_ref):
            if changed > 0:
                block_size -= changed
                break
            else:
                changed = block_size
        ct_ref = new_ct
        block_size += 1
            
    return block_size

if __name__ == "__main__":
    recovered = b''
    p = log.progress(f'working...')

    block_size = determine_block_size()
    info(f"Block size: {block_size}")
    window = (len(encrypt('00')) // block_size) * block_size
    while True: 
        padding = b'A'*(window - 1 - len(recovered))
        ref = encrypt(padding.hex())
        for c in range(256):
            ct = encrypt((padding+recovered+bytes([c])).hex())
            p.status(f"\n  ct: {ct[window-block_size:window].hex()}\n ref: {ref[window-block_size:window].hex()}\nflag: {recovered}\n pad: {(padding+recovered+bytes([c])).hex()}")
            if ct[window-block_size:window] == ref[window-block_size:window]:
                recovered += bytes([c])
                break
        
        if len(SECRET) == len(recovered):
            break

    success(recovered)