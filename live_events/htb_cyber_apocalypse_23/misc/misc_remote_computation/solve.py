from pwn import *

# Allows you to switch between local/GDB/remote from terminal
def start(argv=[], *a, **kw):
    if args.REMOTE:  # ('server', 'port')
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:  # Run locally
        info("Error: Invalid args!")
        exit()

context.log_level = 'debug'

io = start()

io.sendlineafter('>', '1')
for _ in range(500):
    io.recvuntil(']:')
    expr = io.recvlineS().strip()[:-4]
    try:
        solution = eval(expr)
        if solution > 1337 or solution < -1337:
            io.sendlineafter('>', 'MEM_ERR')
        else:
            io.sendlineafter('>', str(round(solution, 2)))
    except ZeroDivisionError:
        io.sendlineafter('>', 'DIV0_ERR')
    except SyntaxError:
        io.sendlineafter('>', 'SYNTAX_ERR')
    
success(io.recvlineS())
io.interactive()