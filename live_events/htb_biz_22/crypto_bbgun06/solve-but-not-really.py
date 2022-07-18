from pwn import *
"""
Not sure why this script doesn't work but there's no validation on the 
server in the original one to prevent people from just reusing the valid
signature. The challenge was later patched to require actual forgery.
"""
context.log_level = 'debug'
r = remote('178.128.162.91', 30529)

r.recvuntil(b'signature: ')
sig = r.recv()

r.recvuntil(b'Enter the signature as hex:')
r.sendline(sig)
flag = r.recvlineS()
success(flag)