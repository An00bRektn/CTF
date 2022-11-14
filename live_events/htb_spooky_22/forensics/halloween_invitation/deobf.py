#!/usr/bin/env python3
import re

pattern = r'uxdufnkjlialsyp\("[0-9]+"\)'
with open('ThisDocument.vba', 'r') as fd, open('ThisDoc-deobf.vba', 'w') as fd2:
    stuff = fd.read()
    funcs = re.findall(pattern, stuff)

    for f in funcs:
        hexstring = bytes.fromhex(f[17:-2]).decode('latin-1')
        stuff = stuff.replace(f, f'{hexstring}')
    
    fd2.write(stuff)

"""
From here, the powershell payload is encoded in decimal (apparently the & operator concatenates digits???), so clean that up, stick it in cyberchef, decode from base64, not worth the time to automate it
"""