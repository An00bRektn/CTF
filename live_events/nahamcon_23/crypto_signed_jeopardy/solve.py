from pwn import *
from math import gcd
from hashlib import sha512
from sage.all import *

context.log_level = 'debug'

# Allows you to switch between local/GDB/remote from terminal
def start(argv=[], *a, **kw):
    if args.REMOTE:  # ('server', 'port')
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:  # Run locally
        return exit() #process([exe] + argv, *a, **kw)

# taken from https://github.com/jvdsn/crypto-attacks/blob/master/attacks/ecc/ecdsa_nonce_reuse.py
def solve_congruence(a, b, m):
    """
    Solves a congruence of the form ax = b mod m.
    :param a: the parameter a
    :param b: the parameter b
    :param m: the modulus m
    :return: a generator generating solutions for x
    """
    g = gcd(a, m)
    a //= g
    b //= g
    n = m // g
    for i in range(g):
        yield (pow(a, -1, n) * b + i * n) % m

def attack(n, m1, r1, s1, m2, r2, s2):
    """
    Recovers the nonce and private key from two messages signed using the same nonce.
    :param n: the order of the elliptic curve
    :param m1: the first message
    :param r1: the signature of the first message
    :param s1: the signature of the first message
    :param m2: the second message
    :param r2: the signature of the second message
    :param s2: the signature of the second message
    :return: generates tuples containing the possible nonce and private key
    """
    for k in solve_congruence(int(s1 - s2), int(m1 - m2), int(n)):
        for x in solve_congruence(int(r1), int(((k * s1)%int(n)) - m1), int(n)):
            yield int(k), int(x)

def verify_sig(m, sig, n, G, pubkey):
    s1 = pow(sig[1], -1, n)
    R = (m * s1) * G + (sig[0] * s1) * pubkey
    #print(R)
    r_prime = R[0]
    return sig[0] == r_prime

p = 6864797660130609714981900799081393217269435300143305409394463459185543183397656052122559640661454554977296311391480858037121987999716643812574028291115057151
a = 6864797660130609714981900799081393217269435300143305409394463459185543183397656052122559640661454554977296311391480858037121987999716643812574028291115057148
b = 1093849038073734274511112390766805569936207598951683748994586394495953116150735016013708737573759623248592132296706313309438452531591012912142327488478985984
Gx = 2661740802050217063228768716723360960729859168756973147706671368418802944996427808491545080627771902352094241225065558662157113545570916814161637315895999846
Gy = 3757180025770020463545507224491183603594455134769762486694567779615544477440556316691234405012945539562144444537289428522585666729196580810124344277578376784
n = 6864797660130609714981900799081393217269435300143305409394463459185543183397655394245057746333217197532963996371363321113864768612440380340372808892707005449
E = EllipticCurve(GF(p), [a, b])
G = E(Gx, Gy)

io = start()
io.recvlineS()
io.recvlineS()

#pubkey = io.recvlineS() + io.recvlineS()
#print(pubkey)
#dGx, dGy = [int(x.strip()) for x in pubkey[14:-1].split(':')][:-1]
#print((dGx, dGy))
dGx = int(input('dGx> '))
dGy = int(input('dGy> '))
pub_pt = E(dGx, dGy)
#exit()

io.sendlineafter('3. Quit', '1')
info(f"Quebbin 1: {io.recvlineS()}")
io.recvuntil('signature: ')
sig1 = eval(io.recvlineS())

is_correct = False

while not is_correct:
    msg1 = "What is "+input("Answer? ").strip().upper()+"?"
    info(f"Answer 1: {msg1}")
    msg1 = int(sha512(msg1.encode()).hexdigest(), 16)
    is_correct = verify_sig(msg1, sig1, n, G, pub_pt)

io.sendlineafter('3. Quit', '1')
info(f"Quebbin 2: {io.recvlineS()}")
io.recvuntil('signature: ')
sig2 = eval(io.recvlineS())
is_correct = False

while not is_correct:
    msg2 = "What is "+input("Answer? ").strip().upper()+"?"
    info(f"Answer 2: {msg2}")
    msg2 = int(sha512(msg2.encode()).hexdigest(), 16)
    is_correct = verify_sig(msg2, sig2, n, G, pub_pt)

info(f"Msg 1: {msg1}")
info(f"Msg 2: {msg2}")
info(f"Sig 1: {sig1}")
info(f"Sig 2: {sig2}")

sols = list(attack(n, msg1, sig1[0], sig1[1], msg2, sig2[0], sig2[1]))
k, d = sols[0]
info(f"Nonce and Private Key: {sols}")
print("=========================== TESTS ===========================")
try:
    assert d*G == pub_pt
except AssertionError:
    info("fail! d value is not correct")

try:
    m = msg1
    P = k*G
    r = int(P[0]) % n
    s = int(((m + (r*d))/k)%n)
    assert r == sig1[0]
    info("r1 is correct")
    assert s == sig1[1]
    info("s1 is correct")
except AssertionError:
    info("fail! Failed to sign first message!")

try:
    m = msg2
    P = k*G
    r = int(P[0]) % n
    s = int(((m + (r*d))/k)%n)
    assert r == sig2[0]
    info("r2 is correct")
    assert s == sig2[1]
    info("s2 is correct")
except AssertionError:
    info("fail! Failed to sign second message!")
print("=========================== TESTS ===========================")

io.sendlineafter('3. Quit', '2')
forged_msg = 'I want to just leave forever and ever'
m = int(sha512(forged_msg.encode()).hexdigest(), 16)
P = k*G
r = int(P[0]) % n
s = int(((m + (r*d))*pow(k, -1, n))%n)

info(f'Forged: {(r,s)}')

io.sendlineafter('Please give the message', forged_msg)
io.sendlineafter('Please give the r value of the signature', str(r))
io.sendlineafter('Please give the s value of the signature', str(s))

io.interactive()