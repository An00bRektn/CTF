from Crypto.Cipher import AES

k = b'supersecretkeyusedforencryption!'
iv = b'someinitialvalue'
ct = bytes.fromhex('5f558867993dccc99879f7ca39c5e406972f84a3a9dd5d48972421ff375cb18c')

cipher = AES.new(k, AES.MODE_CBC, iv=iv)
print(f'[+] {cipher.decrypt(ct).decode()}')