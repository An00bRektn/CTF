from Crypto.Cipher import AES
from os import urandom
from utils import *
import json

class WebApp:
    def __init__(self):
        self.KEY = urandom(16)
        self.FLAG = 'pals{7h1s_1s_4_m4d3_up_fl4g}'
        self.UID = 10

    def parse_cookie(self, cookie: str):
        user = dict([key_val.split('=') for key_val in cookie.split('&')])
        return json.dumps(user)

    def profile_for(self, email: str):
        email = email.replace('&', '%26').replace('=','%3d')
        cookie = f'email={email}&uid={self.UID}&role=user'.encode('latin-1')
        self.UID += 1
        cipher = AES.new(self.KEY, AES.MODE_ECB)
        return cipher.encrypt(pkcs7_pad(cookie)).hex()
        
    def validate_login(self, cookie):
        cookie = bytes.fromhex(cookie)
        cipher = AES.new(self.KEY, AES.MODE_ECB)
        try:
            cookie = json.loads(self.parse_cookie(unpad(cipher.decrypt(cookie)).decode('latin-1')))
        except Exception as e:
            return f'Invalid cookie: {e}'
        try:
            if cookie['role'] == 'admin':
                return f'Welcome admin, here is your flag: {self.FLAG}'
            elif cookie['role'] == 'user':
                username = cookie['email']
                return f'Welcome {username}'
            else:
                return f'Invalid cookie'
        except:
            return 'Error: no role field found'

if __name__ == "__main__":
    """
    email=admin&uid=10&role=user
    email=AAAAAAAAAAadmin\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b&uid=10&role=user

    email={13 bytes}&uid=10&role={admin_block}
    """
    app = WebApp()
    extract_cookie = app.profile_for('A'*10 + 'admin' + (b'\x0b'.decode('latin-1') * 11))
    admin_block = extract_cookie[32:64]
    forged = app.profile_for('notanadmin420')[:64] + admin_block
    print(app.validate_login(forged))
    
