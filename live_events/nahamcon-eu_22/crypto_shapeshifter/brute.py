from Crypto.Util.number import bytes_to_long as b2l

class LFSR():
    def __init__(self, iv):
        self.state = [int(c) for c in iv]
        #self.state = self.iv

    def shift(self):
        s = self.state
        newbit = s[15] ^ s[13] ^ s[12] ^ s[10] # ^ s[0]
        s.pop()
        self.state = [newbit] + s

with open("output.txt", 'r') as fd:
    enc = [x.strip() for x in fd.readlines()]

FLAG = b'flag{xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx}'
potential = 'abcdef1234567890'
flag_chars = []
for a in potential:
    for b in potential:
        flag_chars.append((a+b).encode())

real_flag = [0 for _ in range(38)]
real_flag[0] = b'f'
real_flag[1] = b'l'
real_flag[2] = b'a'
real_flag[3] = b'g'

for i in range(0, 38, 2):
    chars = f'{b2l(FLAG[i:i+2]):016b}'
    assert len(chars) == 16
    if i < 4:
        pass
    elif i == 4:
        for guess in potential:
            guess = ('{' + guess).encode()
            chars = f'{b2l(guess):016b}'
            lfsr = LFSR(chars)
            for _ in range(31337):
                lfsr.shift()

            finalstate = ''.join([str(c) for c in lfsr.state])
            if finalstate == enc[i//2]:
                real_flag[i], real_flag[i+1] = bytes([guess[0]]), bytes([guess[1]])
                break

    elif i == 36:
        for guess in potential:
            guess = (guess + "}").encode()
            chars = f'{b2l(guess):016b}'
            lfsr = LFSR(chars)
            for _ in range(31337):
                lfsr.shift()

            finalstate = ''.join([str(c) for c in lfsr.state])
            if finalstate == enc[i//2]:
                real_flag[i], real_flag[i+1] = bytes([guess[0]]), bytes([guess[1]])
                break

    else:
        for guess in flag_chars:
            chars = f'{b2l(guess):016b}'
            lfsr = LFSR(chars)
            for _ in range(31337):
                lfsr.shift()

            finalstate = ''.join([str(c) for c in lfsr.state])
            if finalstate == enc[i//2]:
                real_flag[i], real_flag[i+1] = bytes([guess[0]]), bytes([guess[1]])
                break

a = ""
for c in real_flag:
    a += c.decode()
print(a)