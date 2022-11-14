import random
import itertools

with open('flag.enc', 'rb') as fd:
    res = fd.read()

def encrypt_stage_one(message, key):
    resp = ''
    # for each tuple in u
    for i in key:
        # for j from the ogindex to the length of the message, by step
        for j in range(i, len(message), len(key)):
            resp += message[j]

    return resp

message_enc, seed_enc = res[:-18], res[-18:]
seed = bytearray([0x42 ^ b for b in seed_enc])

random.seed(seed)
key = [random.randrange(256) for _ in message_enc]

decrypt_stage2 = [m ^ k for (m,k) in zip(res, key + [0x42]*len(seed))]
decrypt_stage2 = "".join([chr(i) for i in decrypt_stage2])

garbled_message = decrypt_stage2[:-18]

base_key = [0, 1, 2, 3, 4, 5, 6, 7]
keyspace = list(itertools.permutations(base_key))

"""
for key in keyspace:
    #tmp = "5!K3rn{T_5SA!}0ypC11uu__E__3j5LFI0Esr0m_1!1"
    tmp = "SEKAI{____________________________________}"
    for _ in range(42):
        tmp = encrypt_stage_one(tmp, key)

    if tmp[2] == 'K' and tmp[6]=='{' and tmp[13]=='}' and tmp[10] == 'S' and tmp[11]=='A':
        true_key = key
        print(f"KEY: {key}")
        break
"""
true_key=(6, 3, 7, 4, 2, 1, 0, 5)

# decrypt
def decrypt_stage1(message, key):
    res = ['' for _ in range(len(message))]
    c = 0
    for i in key:
        for j in range(i, len(message), len(key)):
            res[j] = message[c]
            c += 1
    return "".join(res)


for _ in range(42):
    garbled_message = decrypt_stage1(garbled_message, true_key)

print(garbled_message)