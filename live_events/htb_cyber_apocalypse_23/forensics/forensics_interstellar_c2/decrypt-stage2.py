#!/usr/bin/env python3
from Crypto.Cipher import AES
from base64 import b64encode, b64decode
import re

key = b64decode(b'DGCzi057IDmHvgTVE2gm60w8quqfpMD+o8qCBGpYItc=')

with open('./Anni%3fTheda=Merrilee%3fc', 'rb') as fd:
    enc = fd.read()
    enc = b64decode(enc)

cipher = AES.new(key, AES.MODE_CBC, iv=key[:16])
dec = cipher.decrypt(enc)

new_thing = b64decode(dec[16:-16]).decode()
#print(new_thing)
patterns = [
    r'RANDOMURI19901(.*)10991IRUMODNAR',
    r'URLS10484390243(.*)34209348401SLRU',
    r'KILLDATE1665(.*)5661ETADLLIK',
    r'SLEEP98001(.*)10089PEELS',
    r'JITTER2025(.*)5202RETTIJ',
    r'NEWKEY8839394(.*)4939388YEKWEN',
    r'IMGS19459394(.*)49395491SGMI'
]
text9_15 = []
for p in patterns:
    matches = re.findall(p, new_thing)
    #print(matches)
    text9_15.append(matches[0])

new_key = b64decode(text9_15[5])
core_cipher = AES.new(new_key, AES.MODE_CBC, iv=new_key[:16])
with open('artifacts/%3fdVfhJmc2ciKvPOC', 'rb') as fd:
    enc_1 = b64decode(fd.read())

dec_1 = core_cipher.decrypt(enc_1)
dec_1_b64 = b64decode(dec_1[16:-8]).decode()

if dec_1_b64.startswith('multicmd'):
    arr = dec_1_b64.replace('multicmd', '').split("!d-3dion@LD!-d")
    i = 0
    for text3 in arr:
        taskid = text3[:5]
        cmd = text3[5:-5]
        print(f"{taskid}: {cmd[:40]}")
        if cmd.lower().startswith('loadmodule'):
            cmd = cmd.replace('loadmodule','')
            with open(f'payloads/stage_{name}-{i}.dll', 'wb') as fd:
                eq = (4-(len(cmd)%4))
                fd.write(b64decode((cmd+('='*eq)).encode()))
            i += 1

with open('artifacts/%3fdVfhJmc2ciKvPOC(14)', 'rb') as fd:
    enc_2 = b64decode(fd.read())

dec_2 = core_cipher.decrypt(enc_2)
dec_2_b64 = b64decode(dec_2[16:-8]).decode()

if dec_2_b64.startswith('multicmd'):
    arr2 = dec_2_b64.replace('multicmd', '').split("!d-3dion@LD!-d")
    for text3 in arr2:
        taskid = text3[:5]
        cmd = text3[5:-5]
        print(f"{taskid}: {cmd[:40]}")
        if taskid == "00035":
            print(text3)
        if cmd.lower().startswith('loadmodule'):
            cmd = cmd.replace('loadmodule','')
            with open(f'payloads/stage_{name}-{i}.dll', 'wb') as fd:
                eq = (4-(len(cmd)%4))
                fd.write(b64decode((cmd+('='*eq)).encode()))            
            i += 1


def parse_blob(enc: bytes, name: str):
    dec = core_cipher.decrypt(enc)
    dec_b64 = b64decode(dec[16:-8]).decode()

    if dec_b64.startswith('multicmd'):
        arr = dec_b64.replace('multicmd', '').split("!d-3dion@LD!-d")
        i = 0
        for text3 in arr:
            taskid = text3[:5]
            cmd = text3[5:-5]
            print(f"{taskid}: {cmd[:40]}")
            if cmd.lower().startswith('loadmodule'):
                cmd = cmd.replace('loadmodule','')
                with open(f'payloads/stage_{name}-{i}.dll', 'wb') as fd:
                    eq = (4-(len(cmd)%4))
                    fd.write(b64decode((cmd+('='*eq)).encode()))
                i += 1

pngs = ['%3fdVfhJmc2ciKvPOC(1)',
'%3fdVfhJmc2ciKvPOC(15)',
'%3fdVfhJmc2ciKvPOC(17)',
'%3fdVfhJmc2ciKvPOC(23)',
'%3fdVfhJmc2ciKvPOC(3)',
'%3fdVfhJmc2ciKvPOC(5)',]

decrypted = []
for png in pngs:
    with open(f"artifacts/{png}", 'rb') as fd:
        comp = fd.read()[1500:]
    decrypted.append(core_cipher.decrypt(comp))

import gzip

x = gzip.decompress(decrypted[3][16:])

with open('endme/letitbeover', 'wb') as fd:
    fd.write(x)
    