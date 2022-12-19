from sage.all import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import hashlib

# Reference function
def f(i):
    if i < 5:
        return i+1
    
    return 1905846624*f(i-5) - 133141548*f(i-4) + 3715204*f(i-3) - 51759*f(i-2) + 360*f(i-1)

# A = diagonlized matrix
# n = nth term
# v_{n+1} = A^{n-1}v_4
def compute_f(A, n):
    v_4 = Matrix(SR, [
        [f(4)],
        [f(3)],
        [f(2)],
        [f(1)],
        [f(0)]
    ])
    return A**(n-1) * v_4

# Create a matrix from the recurrence
# and then diagonalize the matrix
A = Matrix(SR, [
    [360, -51759, 3715204, -133141548, 1905846624],
    [1, 0, 0, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 1, 0]
    ])

eigenvalues = A.eigenvalues()

d = [[0 for _ in range(5)] for __ in range(5)]
for i,e in enumerate(eigenvalues):
    d[i][i] = e

D = Matrix(SR, d)

eigenv_right = A.eigenvectors_right()
p_tmp = [list(x[1][0]) for i,x in enumerate(eigenv_right)]
p = [[0 for _ in range(5)] for __ in range(5)]
for i in range(5):
    for j in range(5):
        p[i][j] = p_tmp[j][i]

P = Matrix(SR, p)
Diag = P*D*P.inverse()
assert Diag == A

num = int(compute_f(Diag, 13371337-3)[0][0])

ENC_MSG = open('msg.enc', 'rb').read()
NUM_HASH = "636e276981116cf433ac4c60ba9b355b6377a50e"

# Decrypt the flag
def decrypt_flag(sol):
    sol = sol % pow(10,31337)
    sol = str(sol)
    num_hash = hashlib.sha1(sol.encode()).hexdigest()
    key = hashlib.sha256(sol.encode()).digest()

    if num_hash != NUM_HASH:
        print('number not computed correctly')
        exit()

    iv = b'\x00'*16
    cipher = AES.new(key, AES.MODE_CBC, iv)
    #print(len(unpad(ENC_MSG)))
    msg_dec = cipher.decrypt(ENC_MSG)
    print(msg_dec)

decrypt_flag(num)

"""
b'Nice job. Matrix diagonalization is pretty cool! Here is your flag for all of the hard work you did:\n\nflag{3f04dfb7f06a4d57a6b6150bdd61dfcd}\x04\x04\x04\x04'
"""