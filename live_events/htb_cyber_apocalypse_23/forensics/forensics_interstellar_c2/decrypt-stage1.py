#!/usr/bin/env python3
from Crypto.Cipher import AES

with open('94974f08-5853-41ab-938a-ae1bd86d8e51', 'rb') as fd:
    enc = fd.read()

key = bytes.fromhex('00010100000101000001010001010000')
iv = bytes.fromhex('00010100000000010001010000010101')
cipher = AES.new(key, AES.MODE_CBC, iv=iv)
dec = cipher.decrypt(enc)
with open('./tmp7102591.exe', 'wb') as fd:
    fd.write(dec)