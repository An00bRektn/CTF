from Crypto.Cipher import AES
from base64 import b64decode

with open('./input-files/7.txt', 'r') as f:
    ct = b64decode(f.read().replace('\n', ''))

KEY = b"YELLOW SUBMARINE"
cipher = AES.new(KEY, AES.MODE_ECB)
print(cipher.decrypt(ct))