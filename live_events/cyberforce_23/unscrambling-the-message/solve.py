#!/usr/bin/python3
# @author: CryptoCat (https://github.com/Crypto-Cat/CTF/tree/main/pwn)
# Modified by An00bRektn
from pwn import *

# BOILERPLATE CODE #
# Allows you to switch between local/GDB/remote from terminal
def start(argv=[], *a, **kw):
    if args.GDB:  # Set GDBscript below
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    else:  # Run locally
        return process([exe] + argv, *a, **kw)

# Specify GDB script here (breakpoints etc)
gdbscript = '''
continue
'''.format(**locals())

# Binary filename
exe = './malware'
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Change logging level to help with debugging (error/warning/info/debug)
context.log_level = 'debug'

##########
# Start Solve

io = start()
io.sendlineafter('Encrypt or Decrypt?', 'Decrypt')
io.sendlineafter('Value to Decrypt?', 'nrp!n3sCUyf1Ion')
# Found hardcoded in check_password() in binary
io.sendlineafter('What is the decryption password?', 'YouFoundThePassword!')
io.recvlineS()
flag = io.recvlineS()
success(flag.split(':')[1].strip())