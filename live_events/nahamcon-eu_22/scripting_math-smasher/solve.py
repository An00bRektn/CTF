#!/usr/bin/python3
# flag{b7e5881388851dda407ce26c4501c887}
import cv2
import urllib
import requests
import numpy as np
import pytesseract
import re

url = "http://challenge.nahamcon.com:32463"
counter_prev = -1
# this is bad but shut up I don't want to use soup
def clean_html(html):
    clean = re.compile("<.*?>")
    return re.sub(clean, '', html)

if __name__ == "__main__":
    while True:
        # Reading image from web instead of downloading
        req = urllib.request.urlopen(url + "/static/eqn.png")
        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
        img = cv2.imdecode(arr, -1)

        # Filtering
        kernel = np.ones((2,1), np.uint8)
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        gray, img_bin = cv2.threshold(gray,128,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        gray = cv2.bitwise_not(img_bin)

        img = cv2.erode(gray, kernel, iterations=1)
        img = cv2.dilate(img, kernel, iterations=1)
        text = pytesseract.image_to_string(img).strip()
        try:
            text = text.replace('°', '*').replace(' ', '').replace('"', '*')
            # praying that blacknote didn't throw a code execution payload
            # in the mix
            solve = eval(text) 
        except Exception:
            print(text)

        # god they made the specifics on how to submit an answer so
        # complicated
        if type(solve) is float:
            solve = str(round(solve, 4))

        # Making the request
        data = dict(eqn_ans=solve)
        requests.post(url=url, data=data)
        check = requests.get(url)
        counter = int(clean_html(check.text).split("}")[4].strip())
        print(f"[+] Inputting: {text} = {solve}, counter now at {counter}")
        
        # Debug failed OCR requests
        if counter_prev > counter:
            cv2.imwrite("fail.png", img)
            exit()

        counter_prev = counter
        
        # This below bit didn't actually work
        # But luckily if you hit 101, just open a browser and go to
        # the page and you'll see the flag pop up
        try:
            # Reading image from web instead of downloading
            req_flag = urlopen(url + "/static/flag.png")
            arr_flag = np.asarray(bytearray(req_flag.read()), dtype=np.uint8)
            img_flag = cv2.imdecode(arr_flag, -1) # 'Load it as it is'
            cv2.imwrite("flag.png", img_flag)
            print(f"[+] DONE! Iterations: {counter}")

            real_flag_img = cv2.imread("flag.png")
            flag_text = pytesseract.image_to_string(real_flag_img)
            print(f"[+] FLAG: {flag_text}")
        except Exception:
            pass