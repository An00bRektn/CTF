# Baby RSA Quiz
## Answers
1: 1751476325 (hehe)
2: 298062599825784604055397390266655425259311588881437826967301557850952291872230439875703282133697119479127924133583415243365 (smol e do be efficient, but smol e do not be secure)
3: 4389692525618482461496676054452486268288388260878585075412513298672841265430477651614481831919140832735218408683300129 (ohhhh nooooo my primessss, they're too closeeeee!)

## The TL;DR on the Weaknesses
1. The numbers selected were just too small. RSA depends on the assumption that large primes are hard to factor, and those numbers, in the realm of cryptography, were small.
2. Small exponent. Technically speaking, 3 as an exponent is not insecure, but because the n is so large, and the plaintext is so small, the public exponent isn't really doing any work at all, because it never wraps around the modulus, so we can just take the cube root.
3. I used RSACtfTool here, and this is the method listed by the tool: "[*] Attack success with SQUFOF method !". I'm still new to cryptography, so I have yet to really understand what happened here, but I highly recommend you watch [Hilbert](https://youtu.be/oSeoLqJ2V7M?t=1132) who knows way more about this than I do 