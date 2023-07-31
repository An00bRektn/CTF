# crypto/fizzbuzz100
flag: `corctf{h4ng_0n_th15_1s_3v3n_34s13r_th4n_4n_LSB_0r4cl3...4nyw4y_1snt_f1zzbuzz_s0_fun}`

You basically get a near-arbitrary RSA decryption oracle, so if you submit the ciphertext $c' \equiv 2^e * c \pmod{n}$, then the server computes: $$\begin{align*}m' \equiv (c')^d \equiv (2^e * c)^d \equiv (2^e * m^e)^d \equiv 2m \pmod{n}\end{align*}$$, and we can compute $m$ from $2m$.