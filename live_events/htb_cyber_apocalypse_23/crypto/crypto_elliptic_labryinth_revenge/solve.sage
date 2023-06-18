from pwn import *
from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Util.number import long_to_bytes
from sage.all import *
import json

load('coppersmith.sage')

# Allows you to switch between local/GDB/remote from terminal
def start(argv=[], *a, **kw):
    if args.REMOTE:  # ('server', 'port')
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:  # Run locally
        print("[!] Error: Insufficient args")

context.log_level = 'debug'
io = start()

def get_truncated_params():
    io.sendlineafter(">", "1")
    output = json.loads(io.recvlineS().strip())
    return int(output["p"], 16), int(output["a"], 16), int(output["b"], 16) 


def get_encrypted_flag():
    io.sendlineafter(">", "2")
    output = json.loads(io.recvlineS().strip())
    return bytes.fromhex(output["iv"]), bytes.fromhex(output["enc"])

io.recvlineS()
init_point = json.loads(io.recvlineS().strip())
x, y = int(init_point["x"], 16), int(init_point["y"], 16)

solved = False

while not solved:
    #good = False
    #while not good:
    p, a_t, b_t = get_truncated_params()
        #if a_t.bit_length() >= 300:
        #    good = True
        #    break

    # We're modeling the truncated integer as subtraction, which is correct
    # but we also need to remember that the actual integer that's being deducted
    # is coming off of a 512 bit number
    aa_t = int(a_t) << (512-int(a_t).bit_length())
    bb_t = int(b_t) << (512-int(b_t).bit_length())

    load('./coppersmith.sage')

    R.<da,db> = PolynomialRing(Zmod(p))
    f = x**3 + (da+aa_t)*x + (db+bb_t) - y**2
    a_0, b_0 = small_roots(f, [2**512,2**512], d=2)[0]

    a = a_0 + aa_t
    b = b_0 + bb_t 
    #(y**2 - x**3 - (a*x)) % p

    # info(f"x = {hex(x)}")
    # info(f"y = {hex(y)}")
    # info(f"a = {hex(a)}")
    # info(f"b = {hex(b)}")
    # info(f"p = {hex(p)}")

    #assert bin(a_t)[2:2+a_t.bit_length()] == bin(a)[2:a_t.bit_length()+2]
    #assert (y**2 % p) == (x**3 + (a*x) + b) % p 
    #assert int(a) >> (512-a_t.bit_length()) == a_t
    #assert int(b) >> (512-b_t.bit_length()) == b_t

    iv, ct = get_encrypted_flag()
    key = sha256(long_to_bytes(pow(int(a), int(b), int(p)))).digest()[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    flag = cipher.decrypt(ct)
    info(flag)
    if flag[0:3] == b'HTB':
        success(flag)
        solved = True
        break