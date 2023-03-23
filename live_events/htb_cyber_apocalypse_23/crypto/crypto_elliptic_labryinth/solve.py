from pwn import *
from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Util.number import long_to_bytes
import json

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

def get_random_point():
    io.sendlineafter(">", "2")
    output = json.loads(io.recvlineS().strip())
    return int(output["x"], 16), int(output["y"], 16)

def get_encrypted_flag():
    io.sendlineafter(">", "3")
    output = json.loads(io.recvlineS().strip())
    return bytes.fromhex(output["iv"]), bytes.fromhex(output["enc"])

x_1, y_1 = get_random_point()
x_2, y_2 = get_random_point()
p, a_trun, b_trun = get_truncated_params()

# Why use coppersmith when you gave me two points LMAO
a = pow(x_1 - x_2, -1, p) * (pow(y_1, 2, p) - pow(y_2, 2, p) - (pow(x_1, 3, p) - pow(x_2, 3, p))) % p
b = (pow(y_1, 2, p) - pow(x_1, 3, p) - a * x_1) % p

iv, ct = get_encrypted_flag()
key = sha256(long_to_bytes(pow(a, b, p))).digest()[:16]
cipher = AES.new(key, AES.MODE_CBC, iv)
flag = unpad(cipher.decrypt(ct), 16)
success(flag)