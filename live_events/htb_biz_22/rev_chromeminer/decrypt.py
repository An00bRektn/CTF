from Crypto.Cipher import AES

# in strings.txt, the output of consolelog-hell.js
ct = bytes.fromhex("E242E64261D21969F65BEDF954900A995209099FB6C3C682C0D9C4B275B1C212BC188E0882B6BE72C749211241187FA8")
iv = key = b"_NOT_THE_SECRET_"

cipher = AES.new(key, AES.MODE_CBC, iv)
pt = cipher.decrypt(ct)
print(pt.decode('utf-8'))