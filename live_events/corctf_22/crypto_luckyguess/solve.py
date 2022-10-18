from pwn import *

context.log_level = 'debug'
r = remote("be.ax", 31800)

r.recvuntil(b"a = ")
a = int(r.recvlineS())

r.recvuntil(b"b = ")
b = int(r.recvlineS())
p = 2**521 - 1

info(f"a = {a}")
info(f"b = {b}")
x = (b * pow((1-a), -1, p)) % p
r.sendlineafter(b'enter your starting point:', str(x))
r.sendlineafter(b'alright, what\'s your guess?', str(x))

flag = r.recvlineS()
success(flag)