#!/usr/bin/env python3
# Automated solver
from pwn import *

# Allows you to switch between local/GDB/remote from terminal
def start(argv=[], *a, **kw):
    return process([exe] + argv, *a, **kw)

# Binary filename
exe = './padlock'
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Change logging level to help with debugging (error/warning/info/debug)
context.log_level = 'debug'

io = start()

# found via ghidra reversing
password = "master locks arent vry strong are they"
password = password.replace("e", "3").replace("o", "0").replace(" ", "_").replace("a", "4")
info(f"password: {password}")

io.sendline(password)
for _ in range(13):
    io.recvlineS()

# ignore the gross output
flag = io.recvall()
success(flag)
print("")