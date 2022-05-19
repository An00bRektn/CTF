# https://gist.github.com/mcieno/f0c6334af28f60d244fa054f5a1c22d2
# Curve parameters
p = 434252269029337012720086440207
a, b = -35, 98

# Target secret key
# d = 8

# Setup curve
E = EllipticCurve(GF(p), [a, b])
G = E(16378704336066569231287640165, 377857010369614774097663166640) #E.gen(0)

P = E(0x9662a556aabae2b203c93040, 0x552c1a38052d0c48baf776f35)
Q = E(0x277d6691d8586f605e8a0350f, 0x3ac1fe3cc66c7d17d1a1e1e11)

# Find the embedding degree
# p**k - 1 === 0 (mod order)
order = E.order()
k = 1
while (p**k - 1) % order:
    k += 1

K.<a> = GF(p**k)
EK = E.base_extend(K)
PK = EK(P)
GK = EK(G)
QK = EK.lift_x(a + 2)  # Independent from PK
AA = PK.tate_pairing(QK, E.order(), k)
GG = GK.tate_pairing(QK, E.order(), k)
dlA = AA.log(GG)

print(dlA)
print(dlA * Q)