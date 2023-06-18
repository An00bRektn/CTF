#!/usr/bin/python3
# @author: CryptoCat (https://github.com/Crypto-Cat/CTF/tree/main/pwn)
# Modified by An00bRektn
from pwn import *

"""
00001004: ca99cd9af6db9acdf69cc1dcddcd99dec7 ^ 0xa9 = c0d3_r3d_5hutd0wn
"""

# Not used, just a reminder for where VM starts
gdbscript = """
break *vm_step+107
c 42
""".format(**locals())

if len(sys.argv) == 1:
    print("[!] Need UWU file to analyze")
    exit()

with open(sys.argv[1], 'rb') as fd:
    uwu = fd.read()[3:]

#with open('./bin-3', 'wb') as fd:
#    fd.write(uwu)

order = ['0000000000101a64', '0000000000101b24', '0000000000101bd9', '0000000000101c99', '0000000000101d4e', '0000000000101e0f', '0000000000101f60', '0000000000101ec5', '000000000010217c', '0000000000102025', '000000000010220c', '0000000000102295', '0000000000102327', '0000000000101415', '00000000001021e2', '00000000001019fc', '00000000001019ae', '0000000000101692', '0000000000101759', '0000000000101820', '00000000001018e7', '00000000001015d2', '0000000000101493', '0000000000101531', '0000000000101433']

pwn_funcs = { 
0x0000000000101415:  "vm_nop",
0x0000000000101433:  "vm_input",
0x0000000000101493:  "vm_store",
0x0000000000101531:  "vm_load",
0x00000000001015d2:  "vm_xor",
0x0000000000101692:  "vm_je",
0x0000000000101759:  "vm_jne",
0x0000000000101820:  "vm_jle",
0x00000000001018e7:  "vm_jge",
0x00000000001019ae:  "vm_putc",
0x00000000001019fc:  "vm_print",
0x0000000000101a64:  "vm_add",
0x0000000000101b24:  "vm_addi",
0x0000000000101bd9:  "vm_sub",
0x0000000000101c99:  "vm_subi",
0x0000000000101d4e:  "vm_mul",
0x0000000000101e0f:  "vm_muli",
0x0000000000101ec5:  "vm_cmp",
0x0000000000101f60:  "vm_div",
0x0000000000102025:  "vm_inv",
0x000000000010217c:  "vm_jmp",
0x00000000001021e2:  "vm_exit",
0x000000000010220c:  "vm_push",
0x0000000000102295:  "vm_pop",
0x0000000000102327:  "vm_mov",
}

original_ops = {}
for addr in order:
    a = int(addr, 16)
    original_ops[a] = pwn_funcs[a]

original_ops = list(original_ops.values())

enc_1 = bytes.fromhex("13190f0a07001d0e16100c010b1f181408091c1a21042212051b1120060215170d1e2303")
enc_2 = bytes.fromhex("16b047b201fbdeeb825d5b5d107c6e215fe7452a3623d4d726d5a311ede75ecbdb9fdde2")
enc_3 = bytes.fromhex("655d774a3340566c75375d356e6e66366c367065776a31795d31707f6c6e33323636315d")


stack = []
registers = [0 for _ in range(0xf)]
def vm_step(i:int, scuff=False):
    opcode = uwu[i]
    if scuff:
        print(f"{hex(i+0x2d0)}: ", end="")
    else:
        print(f"{hex(i)}: ", end="")
    
    if 0x19 < opcode:
        print("dead")
        print(f"[ DEBUG ]: {hex(i)} {hex(i+9)}")
        #exit(0)
        raise Exception

    readable = original_ops[opcode]
    #print(readable)
    if readable == "vm_putc":
        print(f"{readable}\t{bytes([uwu[i+1]])}")
        next_i = i+6
        return next_i, readable, [uwu[i+1]]
    elif readable == "vm_exit":
        print(f"{readable}")
        next_i = i+6
        return next_i, readable, []
    elif readable == "vm_push":
        print(f"{readable}\t{hex(uwu[i+1])}")
        stack.append(uwu[i+1])
        next_i = i+6
        return next_i, readable, [uwu[i+1]]
    elif readable == "vm_mov":
        val = pack(int(uwu[i+2:i+6].hex(),16), endianness="little").hex()
        print(f"{readable}\t{hex(uwu[i+1])} 0x{val}")
        next_i = i+6
        return next_i, readable, [uwu[x] for x in range(i,6)]
    elif readable == "vm_addi":
        print(f"{readable}\t{hex(uwu[i+1])} {hex(uwu[i+2])} {hex(uwu[i+3])}")
        next_i = i+6
        return next_i, readable, [uwu[i+x] for x in range(1,4)]
    elif readable == "vm_store":
        print(f"{readable}\t{hex(uwu[i+1])} {hex(uwu[i+2])}")
        next_i = i+6
        return next_i, readable, [uwu[i+x] for x in range(1,3)]
    elif readable == "vm_load":
        print(f"{readable}\t{hex(uwu[i+1])} {hex(uwu[i+2])}")
        next_i = i+6
        return next_i, readable, [uwu[i+x] for x in range(1,3)]
    else:
        args = [hex(uwu[i+x]) for x in range(1,6)]
        print_args = ""
        for a in args:
            if a != '0x0':
                print_args += f"{a} "
        print(f"{readable}\t{print_args}")
        next_i = i+6
        return next_i, readable, [uwu[x] for x in range(i,6)] 

    
     
    #exit()

def vm_run(i: int, scuff=False):
    if uwu[i+4] == 0:
        next_i, opcode, args = vm_step(i, scuff)
    else:
        return
    
    vm_run(next_i, scuff)
    # match(opcode):
    #     case "vm_putc":
    #         print(args[0], end="")
    #     case other:
    #         print("undefined")
    #         exit()
        
vm_run(0)

# not actually packed just XORed
# 12 am brain go brrr
packed = bytes.fromhex("103c00000000102000000000104500000000106e00000000107400000000106500000000107200000000102000000000107300000000106500000000106300000000107200000000106500000000107400000000102000000000107000000000106800000000107200000000106100000000107300000000106500000000100a00000000103e000000001020000000000c1e301100000c1c000000000c1d24000000181900000000161e19000000011e1e010000011c1c010000131c1d9200000c1c000000000c1d230000000c1e301100000c1f941100000c1a000000000c1b2300000017141e00000017151f0000000a14000000000b13000000000c1230110000001212150000171112000000161e11000000161213000000011a1a010000011e1e010000011f1f010000131a1b9d00000c1e301100000c1ff81100000c1a000000000c1b2300000017141e0000000a1f000000000b0f00000000000f0f1c000017100f000000151414100000161e14000000011a1a010000011e1e010000131a1bae0000011c1c010000131c1d9900000c1e301100000c1f5c1200000c1a000000000c1b23000000170f1e00000017101f000000110f10c90000105700000000107200000000106f00000000106e00000000106700000000102100000000100a000000000e0000000000011a1a010000011e1e010000011f1f010000131a1bbe0000104100000000106300000000106300000000106500000000107300000000107300000000102000000000106700000000107200000000106100000000106e00000000107400000000106500000000106400000000102c00000000102000000000107300000000106800000000107500000000107400000000107400000000106900000000106e00000000106700000000102000000000106400000000106f00000000107700000000106e00000000102100000000100a000000000e0000000000")

uwu = packed
print("-----------------------------------------------")
vm_run(0, True)

"""
"""