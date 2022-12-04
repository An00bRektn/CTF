from pwn import *
from Crypto.Util.Padding import pad

# Allows you to switch between local/GDB/remote from terminal
def start(argv=[], *a, **kw):
    if args.REMOTE:  # ('server', 'port')
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:  # Run locally
        error("Error: Please Specify")

context.log_level = 'debug'
BLOCK_SIZE = 16

def badpad(pt):
    if len(pt) % BLOCK_SIZE != 0:
        pt = pad(pt, BLOCK_SIZE)
    return pt

msg = b'Property: '
coll = badpad(msg).hex()[len(msg)*2:]

io = start()
io.sendlineafter("Property: ", "")
io.sendlineafter("Property: ", coll)
io.recvlineS()
flag = io.recvlineS()
success(flag)
#io.interactive()