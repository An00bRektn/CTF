from os import urandom
from random import choice
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64decode, b64encode

class PaddingOracle:
    def __init__(self) -> None:
        self.KEY = urandom(16)
        self.strings = [
            "MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=",
            "MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=",
            "MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==",
            "MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==",
            "MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl",
            "MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==",
            "MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==",
            "MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=",
            "MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=",
            "MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93"
        ]

    def encrypt(self):
        cipher = AES.new(self.KEY, AES.MODE_CBC)
        iv = urandom(16)
        pt = b64decode(choice(self.strings))
        return b64encode(iv + cipher.encrypt(pad(pt, AES.block_size)))

    def decrypt(self, ct):
        encrypted = b64decode(ct)
        iv, ct = encrypted[:16], encrypted[16:]
        cipher = AES.new(self.KEY, AES.MODE_CBC, iv)
        try:
            pt = unpad(cipher.decrypt(ct), AES.block_size)
            return True
        except:
            return False

if __name__ == "__main__":
    from pwn import *
    from sys import exit

    """
    So for some reason, my code works, but it just doesn't work with the PyCryptodome library I was using
    because I was too lazy to write an actual AES implementation. Not sure why, still need to look into the kinks
    but will update once I have a fix.
    """

    def xor(pt, key):
        if len(key) < len(pt):
            b1, b2 = pt, key
        else:
            b1, b2 = key, pt
        try:
            return bytes([b1[i]^b2[i%len(b2)] for i in range(len(b1))])
        except ZeroDivisionError:
            return b''

    oracle = PaddingOracle()

    encrypted = b64decode(oracle.encrypt())
    ct_blocks = [encrypted[i:i+16] for i in range(16, len(encrypted), 16)]
    pt = b''
    p = log.progress('waiting...')
    init_block = encrypted[:16]
    for i, block in enumerate(ct_blocks):
        intermediate = bytearray([])
        for l in range(1, 17):
            for guess in range(256):
                byte_guess = bytes([guess])
                tampered = urandom(16-l) + byte_guess + xor(intermediate, bytes([l]))
                p.status(f'\n mod: {tampered.hex()}\n int: {intermediate.hex()}\n  pt: {pt.hex()}')
                
                assert len(tampered) % 16 == 0
                if oracle.decrypt(b64encode(tampered + block)):
                    intermediate.insert(0, guess ^ l)
                    break
            else:
                info("Never hit it :(")
                exit()

        pt += xor(intermediate, init_block)
        init_block = block
    
    success(unpad(pt,16).decode('latin-1'))


