from pwn import *

enc_1 = bytes.fromhex("13190f0a07001d0e16100c010b1f181408091c1a21042212051b1120060215170d1e2303")
enc_2 = bytes.fromhex("16b047b201fbdeeb825d5b5d107c6e215fe7452a3623d4d726d5a311ede75ecbdb9fdde2")
enc_3 = bytes.fromhex("655d774a3340566c75375d356e6e66366c367065776a31795d31707f6c6e33323636315d")
possible_chars = [bytes([i]) for i in range(33, 127)]

scrambled = b'g_uH1BTnw5_7lld4n4rguh3{_3r}nl10443_'

def forwards(arr):

    permuted = arr
    for i,p in enumerate(enc_1):
        tmp = permuted[i]
        permuted[i] = permuted[p]
        permuted[p] = tmp

    return permuted

def backwards(arr):
    key = [x for x in enc_1]
    key.reverse()
    unpermute = arr
    for i, p in enumerate(key):
        tmp = unpermute[35-i]
        unpermute[35-i] = unpermute[p]
        unpermute[p] = tmp
        #print(bytes(unpermute).decode())
    return unpermute


#a = [x for x in b'HTB{g_u1nw5_7lld4n4rguh3_3rnl10443_}']
#test = forwards(a)
#print(bytes(test).decode())

test = [x for x in scrambled]
for i in range(100):
    test = backwards(test)
    flag = bytes(test).decode()
    if flag.startswith('HTB{') and flag[-1] == '}':
        print(flag)


"""
[*] 0x402: vm_mov	0x1e 0x00001130
[*] 0x408: vm_mov	0x1f 0x000011f8
[*] 0x40e: vm_mov	0x1a 0x00000000
[*] 0x414: vm_mov	0x1b 0x00000023
[*] 0x41a: vm_load	0x14 0x1e
[*] 0x420: vm_push	0x1f
[*] 0x426: vm_pop	['0xf', '0x0', '0x0', '0x0', '0x0']
[*] 0x42c: vm_add	['0xf', '0xf', '0x1c', '0x0', '0x0']
[*] 0x432: vm_load	0x10 0xf
[*] 0x438: vm_xor	['0x14', '0x14', '0x10', '0x0', '0x0']
[*] 0x43e: vm_store	0x1e 0x14
[*] 0x444: vm_addi	0x1a 0x1a 0x1
[*] 0x44a: vm_addi	0x1e 0x1e 0x1
[*] 0x450: vm_jle	['0x1a', '0x1b', '0xae', '0x0', '0x0']
[*] 0x456: vm_addi	0x1c 0x1c 0x1
[*] 0x45c: vm_jle	0x1c 0x1d '0x99', '0x0', '0x0']
"""