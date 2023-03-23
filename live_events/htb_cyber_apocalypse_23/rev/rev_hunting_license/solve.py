#!/usr/bin/python3
# @author: CryptoCat (https://github.com/Crypto-Cat/CTF/tree/main/pwn)
# Modified by An00bRektn
from pwn import *

"""
Note, flag actually comes from a server that quizzes you
on the binary, but shouldn't be too hard when you know the passwords
from running strings
"""

# Allows you to switch between local/GDB/remote from terminal
def start(argv=[], *a, **kw):
    if args.GDB:  # Set GDBscript below
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:  # ('server', 'port')
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:  # Run locally
        return process([exe] + argv, *a, **kw)

# Specify GDB script here (breakpoints etc)
gdbscript = '''
continue
'''.format(**locals())

# Binary filename
exe = './license'
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Change logging level to help with debugging (error/warning/info/debug)
context.log_level = 'debug'

io = start()
io.sendlineafter(')', 'y')
io.sendlineafter(':', 'PasswordNumeroUno')
io.sendlineafter('?', 'P4ssw0rdTw0')
io.sendlineafter(':', 'ThirdAndFinal!!!')
io.interactive()
# HTB{l1c3ns3_4cquir3d-hunt1ng_t1m3!}