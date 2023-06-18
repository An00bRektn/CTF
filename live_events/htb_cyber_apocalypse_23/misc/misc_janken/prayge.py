from pwn import *
import time
# https://stackoverflow.com/questions/60331996/does-python-have-a-function-to-mimic-the-sequence-of-cs-rand
from ctypes import CDLL

"""
Note, this took like 100 attempts to finally get the flag
I will fight w3th4nds in a denny's parking lot
"""

# Allows you to switch between local/GDB/remote from terminal
def start(argv=[], *a, **kw):
    if args.REMOTE:  # ('server', 'port')
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:  # Run locally
        return process([exe] + argv, *a, **kw)

exe = './janken'
context.log_level = 'debug'

io = start()
libc = CDLL("libc.so.6")
options = ["rock", "scissors", "paper"]
wins = {
    "rock": "paper",
    "scissors": "rock",
    "paper": "scissors"
}

io.sendlineafter('>>', '1')
for i in range(99):
    seed = int(time.time())
    libc.srand(seed)
    op_choice = options[libc.rand() % 3]
    my_choice = wins[op_choice]
    #io.recvuntil('>>')
    info(f"{i}")
    time.sleep(1)
    io.sendline(my_choice)

io.recvuntil("prize: ")
success(io.recvlineS())
io.interactive()