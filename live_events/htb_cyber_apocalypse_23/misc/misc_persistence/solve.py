import sys
import requests as r

if len(sys.argv) != 2:
    print("[!] Error: Invalid args!")
    print("[*] Usage: python3 solve.py IP:PORT")
    exit()

URL = f"http://{sys.argv[1]}/flag"
responses = []
try:
    while True:
        res = r.get(URL)
        responses.append(res.text)
        if 'HTB{' in res.text:
            print("[+] FLAG: {res.text}")
except KeyboardInterrupt:
    with open("res.log", "w") as fd:
        for text in responses:
            fd.write(text+"\n")
    exit()
except Exception:
    exit()
