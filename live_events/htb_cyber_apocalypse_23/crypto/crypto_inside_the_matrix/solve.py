from pwn import *
from sage.all import *

# Allows you to switch between local/GDB/remote from terminal
def start(argv=[], *a, **kw):
    if args.REMOTE:  # ('server', 'port')
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:  # Run locally
        print("[!] Insufficient args!")
        exit()

io = start()

def get_values():
    io.sendlineafter('>', 'C')
    io.recvline()
    ciphertext = eval(io.recvlineS())
    key = eval(io.recvlineS())
    return ciphertext, key

primes = [17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61]

win = False
while not win:
    ciphertext, key = get_values()
    for p in primes:
        ct = matrix(GF(p), 5, 5, ciphertext)
        key = matrix(GF(p), 5, 5, key)

        if key.is_invertible():
            message = ct * key.inverse()
            ints = [val for r in message.rows() for val in r]
            flag = bytes([val for r in message.rows() for val in r])
            #info(f"Potential flag: {flag}")
            if ints[0:4] == [72%p, 84%p, 66%p, 123%p]:
                info(f"Flag: {flag}")
                info(f"Prime: {p}")
                correct_prime = p
                win = True
                break
        else:
            pass
    else:
        io.sendlineafter('>', 'T')

# Generate possibilities for each character
printable_chars = [chr(x).encode() for x in range(33, 127)]
final_flag = [[] for _ in range(25)]
index = 0
for c in flag:
    counter = 1
    while True:
        restored = c + (correct_prime * counter)
        if bytes([restored]) in printable_chars:
            final_flag[index].append(bytes([restored]))
        counter += 1
        if restored > 127:
            break
    index += 1

# Let's play guess the flag!!!
from pprint import pprint
pprint(final_flag)
# HTB{l00k_@t_7h3_st4rs!!!}