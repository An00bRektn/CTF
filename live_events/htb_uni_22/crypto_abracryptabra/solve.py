import logging
import os
import sys
from itertools import combinations
from math import ceil
from math import gcd
from math import sqrt

from sage.all import ZZ
from sage.all import Zmod
from sage.all import factor
from sage.all import matrix

path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(os.path.abspath(__file__)))))
if sys.path[1] != path:
    sys.path.insert(1, path)

from attacks.hnp import lattice_attack
from shared.lattice import shortest_vectors
from shared.polynomial import polynomial_gcd_crt

"""
    The actual attack code for the truncated LCG and Knapsack come from https://github.com/jvdsn/crypto-attacks
    Due to dependencies, here's how you can run this:

        git clone https://github.com/jvdsn/crypto-attacks.git
        cp solve.py crypto-attacks/attacks/lcg; cd crypto-attacks/attacks/lcg
        sage -python solve.py REMOTE 127.0.0.1 1337
"""


# Section 2.1 in "On Stern's Attack Against Secret Truncated Linear Congruential Generators".
def _generate_polynomials(y, n, t):
    B = matrix(ZZ, n, n + t)
    for i in range(n):
        for j in range(t):
            B[i, j] = y[i + j + 1] - y[i + j]

        B[i, t + i] = 1

    x = ZZ["x"].gen()
    for v in shortest_vectors(B):
        P = 0
        for i, l in enumerate(v[t:]):
            P += l * x ** i
        yield P


# Section 4 in "On Stern's Attack Against Secret Truncated Linear Congruential Generators".
def _recover_modulus_and_multiplier(polynomials, m=None, a=None, check_modulus=None):
    for comb in combinations(polynomials, 3):
        P0 = comb[0]
        P1 = comb[1]
        P2 = comb[2]
        m_ = gcd(P0.resultant(P1), P1.resultant(P2), P0.resultant(P2))
        if (m is None and check_modulus(m_)) or m_ == m:
            if a is None:
                factors = factor(m_)
                g = polynomial_gcd_crt(P0, polynomial_gcd_crt(P1, P2, factors), factors)
                for a_ in g.change_ring(Zmod(m_)).roots(multiplicities=False):
                    yield int(m_), int(a_)
            else:
                yield int(m_), a


# Generates possible values for the modulus, multiplier, increment, and seed.
# This is similar to the Hidden Number Problem, but with two 'global' unknowns.
def _recover_increment_and_seed(y, k, s, m, a):
    a_ = []
    b_ = []
    X = 2 ** (k - s)
    mult1 = a
    mult2 = 1
    for i in range(len(y)):
        a_.append([mult1, mult2])
        b_.append(-X * y[i])
        mult1 = (a * mult1) % m
        mult2 = (a * mult2 + 1) % m

    for _, (x0_, c_) in lattice_attack.attack(a_, b_, m, X):
        yield m, a, c_, x0_


def attack(y, k, s, m=None, a=None, check_modulus=None):
    """
    Recovers possible parameters and states from a truncated linear congruential generator.
    More information: Contini S., Shparlinski I. E., "On Stern's Attack Against Secret Truncated Linear Congruential Generators"
    If no modulus is provided, attempts to recover a modulus from the outputs.
    If no multiplier is provided, attempts to recover a multiplier from the outputs.
    Also recovers an increment from the outputs.
    The resulting parameters may not match the original parameters, but the generated sequence should be the same up to some small error.
    :param y: the sequential output values obtained from the truncated LCG (the states truncated to s most significant bits)
    :param k: the bit length of the states
    :param s: the bit length of the outputs
    :param m: the modulus of the LCG (can be None)
    :param a: the multiplier of the LCG (can be None)
    :param check_modulus: a function which checks if a possible value can be the modulus (default: compare the bit length with k)
    :return: a generator generating possible parameters (tuples of modulus, multiplier, increment, and seed) of the truncated LCG
    """
    if m is None or a is None:
        alpha = s / k
        t = int(1 / alpha)
        n = ceil(sqrt(2 * alpha * t * k))

        # We start at the minimum useful chunk size.
        chunk_size = n + t
        while chunk_size <= len(y):
            logging.info(f"Trying chunk size {chunk_size}...")
            polynomials = []
            for i in range(len(y) // chunk_size):
                logging.info(f"Generating polynomials for n = {n}, t = {t}...")
                for P in _generate_polynomials(y[chunk_size * i:chunk_size * (i + 1)], n, t):
                    polynomials.append(P)

            logging.info("Recovering modulus and multiplier...")
            for m_, a_ in _recover_modulus_and_multiplier(polynomials, m, a, check_modulus or (lambda m_: m_.bit_length() == k)):
                logging.info("Recovering increment and seed...")
                yield from _recover_increment_and_seed(y, k, s, m_, a_)

            t += 1
            n = ceil(sqrt(2 * alpha * t * k))
            chunk_size = n + t
    else:
        logging.info("Recovering increment and seed...")
        yield from _recover_increment_and_seed(y, k, s, m, a)

#######################################################################
# BEGIN ACTUAL SOLVE
#######################################################################

from pwn import *

# Allows you to switch between local/GDB/remote from terminal
def start(argv=[], *a, **kw):
    if args.REMOTE:  # ('server', 'port')
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:  # Run locally
        error("Error: Please Specify")

context.log_level = 'info'

io = start()

# Getting a sample of 10 outputs from the LCG
y = []
# 10 is an arbitrary number
for i in range(10):
    io.sendlineafter(">", "1")
    io.recvlineS()
    y.append(int(io.recvlineS()))

BIT_LENGTH_STATE = 127
BIT_LENGTH_OUT = 32
mod = 108314726549199134030277012155370097074
mult = 31157724864730593494380966212158801467

# Using the attack
for a in attack(y, BIT_LENGTH_STATE, BIT_LENGTH_OUT, mod, mult):
    stuff = a

mod_p, mult_p, critChance, spell = stuff

def gen(spell):
    spell = (mult * spell + critChance) % mod
    spellAttack = spell >> (mod.bit_length() - 32)
    return spellAttack, spell

attacks = []
for i in range(10):
    asdf = gen(spell)
    attacks.append(asdf[0])
    spell = asdf[1]

# Verifying that our parameters are correct
assert y == attacks

# Predicting the LCG output
wiz = 200
player = 90
while True:
    attack, spell = gen(spell)
    io.sendlineafter(">", str(attack))
    res = io.recvlineS()
    if 'easy' not in res:
        wiz -= 1
    else:
        player -= 1

    if context.log_level != "debug":
        info(f"Player Health: {player} - Wiz Health: {wiz}")

    if wiz == 0:
        io.recvlineS()
        scroll_len = int(io.recvlineS())
        scroll_pcs = []
        for _ in range(scroll_len):
            scroll_pcs.append(int(io.recvlineS()))
        enc = io.recvlineS()
        break

info(f"scroll length: {scroll_len}")
info(f"encrypted: {enc}")

###############################
# BEGIN PHASE 2
###############################
# Recover the disruptedFlag
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Util.number import bytes_to_long, long_to_bytes

# This is why we had to keep track of health
for _ in range(player):
    attack, spell = gen(spell)
finalattack = attack

finalSpellIngredient = str(finalattack).encode()
finalSpellIngredient = hashlib.md5(finalSpellIngredient).digest()
finalSpell = AES.new(finalSpellIngredient, AES.MODE_CBC)

disruptedFlag = unpad(finalSpell.decrypt(bytes.fromhex(enc)), AES.block_size)

info(f"disrupted flag: {disruptedFlag}")
endme = disruptedFlag[23:].decode()
disrupted = bytes_to_long(bytes.fromhex(endme))

############################
# RECOVER BITS
############################

import os
import sys
from math import ceil
from math import log2
from math import sqrt

from sage.all import QQ
from sage.all import matrix

path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(os.path.abspath(__file__)))))
if sys.path[1] != path:
    sys.path.insert(1, path)

from shared.lattice import shortest_vectors

# Knapsack stuff

def recover_bits(a, s):
    """
    Tries to find e_i values such that sum(e_i * a_i) = s.
    This attack only works if the density of the a_i values is < 0.9048.
    More information: Coster M. J. et al., "Improved low-density subset sum algorithms"
    :param a: the a_i values
    :param s: the s value
    :return: the e_i values, or None if the e_i values were not found
    """
    n = len(a)
    d = n / log2(max(a))
    N = ceil(1 / 2 * sqrt(n))
    assert d < 0.9408, f"Density should be less than 0.9408 but was {d}."

    L = matrix(QQ, n + 1, n + 1)
    for i in range(n):
        L[i, i] = 1
        L[i, n] = N * a[i]

    L[n] = [1 / 2] * n + [N * s]

    for v in shortest_vectors(L):
        s_ = 0
        e = []
        for i in range(n):
            ei = 1 - (v[i] + 1 / 2)
            if ei != 0 and ei != 1:
                break

            ei = int(ei)
            s_ += ei * a[i]
            e.append(ei)

        if s_ == s:
            return e

bits = "".join([str(x) for x in recover_bits(scroll_pcs, disrupted)])
# https://stackoverflow.com/questions/32675679/convert-binary-string-to-bytearray-in-python-3
def bitstring_to_bytes(s):
    v = int(s, 2)
    b = bytearray()
    while v:
        b.append(v & 0xff)
        v >>= 8
    return bytes(b[::-1])

success(f"HTB{(bitstring_to_bytes(bits).decode())}")