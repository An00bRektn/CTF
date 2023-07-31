#!/usr/bin/env python3
from pwn import *
from Crypto.Util.number import long_to_bytes
# corctf{h4ng_0n_th15_1s_3v3n_34s13r_th4n_4n_LSB_0r4cl3...4nyw4y_1snt_f1zzbuzz_s0_fun}
context.log_level = "debug"

def start(argv=[], *a, **kw):
    if args.REMOTE:  # ('server', 'port')
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:  # Run locally
        return process(["python3", "fizzbuzz100.py"])
    
io = start()
n = int(io.recvlineS().split('=')[1].strip())
e = int(io.recvlineS().split('=')[1].strip())
ct = int(io.recvlineS().split('=')[1].strip())

io.sendlineafter(">", str((pow(2,e) * ct)%n))
m_prime = int(io.recvlineS().strip())

print(long_to_bytes((m_prime * pow(2, -1, n))%n))
