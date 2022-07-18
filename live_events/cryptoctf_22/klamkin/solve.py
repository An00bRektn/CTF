from pwn import *
import re

context.log_level = 'debug'


"""
The actual server side response
||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
|  Hello, now we are finding the integer solution of two divisibility  |
|  relation. In each stage send the requested solution. Have fun :)    |
||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
| We know (ax + by) % q = 0 for any (a, b) such that (ar + bs) % q = 0
| and (q, r, s) are given!
| Options: 
|	[G]et the parameters 
|	[S]end solution 
|	[Q]uit
G
| q = 331600439523310363985195296705095144301
| r = 269849536463027367049552375902941847191
| s = 204630480177713496640710480133426306189
| Options: 
|	[G]et the parameters 
|	[S]end solution 
|	[Q]uit
S
| please send requested solution like x, y such that x is 12-bit:
[This continues for varying bit sizes of x or y]
"""

"""
[Explanation]
We are given:
    q,r,s from (ar + bs) % q = 0

And with the unknown a and b, we need to find x and y with various constraints. Obviously r and s
are valid solutions, but to prove we actually *did* anything, we need to do some math to find additional solutions.

We will always set the constrained variable to 2^{BIT_SIZE} - 1 to ensure a valid length.
(Writing all of this out because I'm still not good at modular math)

    ar + bs = 0 mod q
    a = bs/r mod q
    (bs/r)x + by = 0 mod q      <-- a = bs/r mod q (recall that in modular math it's not straight division, it's multiplying by the modular inverse)
    bsx/r = by mod q
    sx/r = y mod q
    sx = ry mod q

Since we are choosing what we set x or y to, we can just rearrange for the other variable. Repeat for
any bit length.
"""

R = remote("04.cr.yp.toc.tf", 13777)

R.recvuntil(b"uit")
R.sendline(b"G")

q,r,s = [int(i) for i in re.findall(b"\d+", R.recvuntil("Options"))]

# Credit to uvicorn from the CryptoHack discord for figuring this one out
def solve_y(bits):
    y = (2 ** bits) - 1
    x = (y * pow(s, -1, q) * r) % q
    return (x,y)

def solve_x(bits):
    x = (2 ** bits) - 1
    y = (x * pow(r, -1, q) * s) % q
    return (x,y)

R.sendline(b"S")

for i in range(5):
    R.recvuntil(b"such that ")
    prompt = R.recvlineS()
    if prompt[0] == "x":
        ans = solve_x(int(re.search(r"[\d]+", prompt).group(0)))
        msg = f"{ans[0]}, {ans[1]}"
        R.sendline(msg.encode('latin-1'))
    else:
        ans = solve_y(int(re.search(r"[\d]+", prompt).group(0)))
        msg = f"{ans[0]}, {ans[1]}"
        R.sendline(msg.encode('latin-1'))

R.recvuntil(b"flag: ")
flag = R.recvlineS()
success(flag)