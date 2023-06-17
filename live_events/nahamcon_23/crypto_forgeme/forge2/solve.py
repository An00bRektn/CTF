from pwn import *
import subprocess

context.log_level == 'debug'

def start(argv=[], *a, **kw):
    if args.REMOTE:  # ('server', 'port')
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:  # Run locally
        return error("Need to specify args!!!")

INJECT = 'https://www.youtube.com/@_JohnHammond'

io = start()

io.recvuntil('first_part:')
first_part = io.recvlineS().strip()

io.sendlineafter('Choice:', '1')
io.sendlineafter('msg (hex):', first_part.encode().hex())
io.recvuntil('H(key || msg):')
tag = io.recvlineS().strip()

info(f"First part: {first_part}")
info(f"Tag: {tag}")
secret_len = None
for i in range(10,120):
    result = subprocess.run(['../hash_extender/hash_extender', '--data', first_part, '--secret', str(i), '--append', f"'{INJECT}'", '--signature', tag, '--format', 'sha1'], stdout=subprocess.PIPE).stdout
    
    sections = result.decode().split('\n')
    forged_tag = sections[2].split(':')[1].strip()
    forged_string = sections[3].split(':')[1].strip()
    #info(f"Forged tag: {forged_tag}")
    #info(f"Forged string: {forged_string}")
    
    io.sendlineafter('Choice:', '2')
    io.sendlineafter('msg (hex):', forged_string)
    io.sendlineafter('tag (hex):', forged_tag)
    if io.recvlineS().strip() == 'True':
        secret_len = i
        info(f"Secret len: {secret_len}")
        break

if secret_len is None:
    error("failure :(")

io.sendlineafter('Choice:', '3')
io.sendlineafter('msg (hex):', forged_string)
io.sendlineafter('tag (hex):', forged_tag)
flag = io.recvlineS()
success(flag)