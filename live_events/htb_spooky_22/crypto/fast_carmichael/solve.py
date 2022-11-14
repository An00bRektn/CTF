#!/usr/bin/env python3
from pwn import *
# https://mathcrypto.wordpress.com/2014/11/29/large-carmichael-numbers-that-are-strong-pseudoprimes-to-several-bases/

context.log_level = 'debug'

# Allows you to switch between local/GDB/remote from terminal
def start(argv=[], *a, **kw):
    if args.REMOTE:  # ('server', 'port')
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:  # Run locally
        print("python3 solve.py REMOTE IP PORT")
        exit()

p = 2887148238050771212671429597130393991977609459279722700926516024197432303799152733116328983144639225941977803110929349655578418949441740933805615113979999421542416933972905423711002751042080134966731755152859226962916775325475044445856101949404200039904432116776619949629539250452698719329070373564032273701278453899126120309244841494728976885406024976768122077071687938121709811322297802059565867

io = start()

io.sendlineafter(':', str(p))
flag = io.recvlineS()
success(flag)