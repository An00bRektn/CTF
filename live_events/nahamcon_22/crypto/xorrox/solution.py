#!/usr/bin/env python3

xorrox=[1, 209, 108, 239, 4, 55, 34, 174, 79, 117, 8, 222, 123, 99, 184, 202, 95, 255, 175, 138, 150, 28, 183, 6, 168, 43, 205, 105, 92, 250, 28, 80, 31, 201, 46, 20, 50, 56]
enc= [26, 188, 220, 228, 144, 1, 36, 185, 214, 11, 25, 178, 145, 47, 237, 70, 244, 149, 98, 20, 46, 187, 207, 136, 154, 231, 131, 193, 84, 148, 212, 126, 126, 226, 211, 10, 20, 119]

def recover_key():
    key = []
    for x in range(len(xorrox)):
        v = 1
        for k in key:
            v ^= k
        if x != 37:
            v ^= xorrox[x+1]
        key.append(v)
    key.insert(0, 124) # Determined by 26 ^ "f"
    return key

def recover_flag():
    plaintext=[]
    key = recover_key()
    print(f"[+] KEY: {key}")

    for i in range(len(enc)):
        plaintext.append(enc[i] ^ key[i])
    flag = [chr(x) for x in plaintext]

    return "".join(flag)

if __name__ == "__main__":
    flag = recover_flag()
    print(f"[+] FLAG: {flag}")
