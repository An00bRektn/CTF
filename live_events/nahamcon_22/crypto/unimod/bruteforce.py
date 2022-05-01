flag = ''
ct = open('out', 'r').read()
for i in range(0xFFFD):
    if chr((ord("f") + i) % 0xFFFD) == ct[0]:
        k = i
        break

print(f"[+] k: {k}")

chars = [chr(x) for x in range(33, 126)]
for c in range(len(ct)):
    for possibly in chars:
        # print(f"Cipher: {ord(ct[c])} -> {((ord(possibly) + k) % 0xFFFD)}")
        if ((ord(possibly) + k) % 0xFFFD) == ord(ct[c]):
            flag += possibly
            break

print(f"[+] FLAG: {flag}")