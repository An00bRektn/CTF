from Crypto.Cipher import AES

with open('encrypted', 'rb') as fd:
    enc = fd.read()

cipher = AES.new(b'you win this ctf', AES.MODE_CBC, iv=enc[:16])

with open('decrypted.jpg', 'wb') as fd:
    dec = cipher.decrypt(enc[16:])
    fd.write(dec)