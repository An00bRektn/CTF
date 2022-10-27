#!/usr/bin/env python3
from pwn import *
import json

context.log_level = 'debug'

# Allows you to switch between local/GDB/remote from terminal
def start(argv=[], *a, **kw):
    if args.REMOTE:  # ('server', 'port')
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:  # Run locally
        print("python3 solve.py REMOTE IP PORT")
        exit()

r = start()

r.sendlineafter(">", '{"option":"3"}')
r.sendlineafter("Expecting modes:", '{"modes":["CTR"]}')

pad = 'A'*100
r.sendlineafter(">", '{"option":"2"}')
r.sendlineafter("plaintext:", '{"plaintext":"'+pad+'"}')
r.recvlineS()
r.recvlineS()
ct1 = bytes.fromhex(json.loads(r.recvlineS())['ciphertext'])

r.sendlineafter(">", '{"option":"1"}')
r.recvlineS()
flag_enc = bytes.fromhex(json.loads(r.recvlineS())['ciphertext'])

msg = xor(xor(ct1, pad), flag_enc)

success(msg)

r.interactive()