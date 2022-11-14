#!/usr/bin/env python3
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
exe = './meeting'
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'debug'

# obtained via strings
passwd = "sup3r_s3cr3t_p455w0rd_f0r_u!"

io = start()

io.sendlineafter('"What is the password for this week\'s meeting?"', passwd)
io.sendlineafter('..."', "cat flag.txt")
io.interactive()
