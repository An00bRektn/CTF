# Brief Writeup
> Credit to [jvdsn](https://github.com/jvdsn/crypto-attacks) for saving me some time having to implement these things

This challenge was basically two challenges.

## Part 1: Truncated LCG
You start with 100 health, the opponent starts with 200. They have an LCG running in the background where they cut off a consistent number of bits. Your job is to predict what they'll do next.

The crypto-attacks repo mentioned above has an attack detailed in `Contini S., Shparlinski I. E., "On Stern's Attack Against Secret Truncated Linear Congruential Generators"` (according to the source code). Just take a sample of about 10 outputs, and fill in the parameters.

This will occasionally fail - just rerun the script until it works. We're then given a `scrollOfWorthiness` (public key) and an encrypted output.

## Interlude: Decrypting The Disrupted Flag
The disrupted flag is encrypted like so:
```python
for _ in range(playerHealth):
    self.spell = (self.armor * self.spell +
                    self.critChance) % self.magicka

finalSpellIngredient = str(self.spell >> (self.magicka.bit_length() -
                                            self.stamina)).encode()
finalSpellIngredient = hashlib.md5(finalSpellIngredient).digest()
finalSpell = AES.new(finalSpellIngredient, AES.MODE_CBC)
disruptedFlag = finalSpell.encrypt(
    pad("You're a wizard Harry, ".encode() + disruptedFlag.encode(),
        AES.block_size)).hex()
```

So the key is just the truncated LCG looped for how ever many hit points we have. Since the Wizard has an ego, they let us know whether our predictions were successful or not, so we can easily keep track of our health, and knowing the paramters, we can just reverse the process.

```python
# This is why we had to keep track of health
for _ in range(player):
    attack, spell = gen(spell)
finalattack = attack

finalSpellIngredient = str(finalattack).encode()
finalSpellIngredient = hashlib.md5(finalSpellIngredient).digest()
finalSpell = AES.new(finalSpellIngredient, AES.MODE_CBC)

disruptedFlag = unpad(finalSpell.decrypt(bytes.fromhex(enc)), AES.block_size)

info(f"disrupted flag: {disruptedFlag}")
endme = disruptedFlag[23:].decode()
disrupted = bytes_to_long(bytes.fromhex(endme))
```

## Part 2: Knapsack
TL;DR: Run another script from the crypto-attacks repo, get bits, profit

The scroll is constructed through doing a bunch of stuff to some random numbers that we can't predict or control, so the important part is this:

```python
# n is the number of bits in the flag string, minus the HTB{} bit
for i in range(self.n):
    scrollOfWorthiness.append(x2 * intList[i] % x1)
```

We generate two constants, `x1` and `x2`, and then get a list of numbers of $x_2a_i \pmod{x_1} \equiv s_i$, where $a_i$ is a random number from 1 to n, and $s_i$ is an entry in the "scroll". This scroll then gets used in the `disrupt()` function.

```python
def disrupt(self, scrollOfWorthiness, flag_bits):
    disruptedFlag = 0

    for i in range(len(flag_bits)):
        if int(flag_bits[i]) != 0: disruptedFlag += scrollOfWorthiness[i]

    return long_to_bytes(disruptedFlag).hex()
```

So basically our problem statment is this:
- We have a list of (for all intents and purposes) random numbers, i.e. the scroll
- The disrupted flag is the sum of some subset of the entries in the scroll. This subset corresponds to the index of each '1' bit in the flag

```
example:
flag_bits = 10110100
list = [1,2,3,4,5,6,7,8]
sum = 14 = 1 + 3 + 4 + 6
```

- If we find the subset, we can see how it lines up with the scroll, and then translate from binary to ascii to get the flag.

This problem is a variant of the [Knapsack](https://en.wikipedia.org/wiki/Knapsack_problem), which is known to be hard. But since the subset is "low density" (no idea what that means lmao), this is actually solvable.

> Read CryptoHack's writeup on [Namura](https://blog.cryptohack.org/cryptoctf2020#namura) from the 2020 CryptoCTF for a similar challenge and a better explanation.

We use another attack from the crypto-attacks repo to pull the bits, and then fully recover the flag.

```python
bits = "".join([str(x) for x in recover_bits(scroll_pcs, disrupted)])
# https://stackoverflow.com/questions/32675679/convert-binary-string-to-bytearray-in-python-3
def bitstring_to_bytes(s):
    v = int(s, 2)
    b = bytearray()
    while v:
        b.append(v & 0xff)
        v >>= 8
    return bytes(b[::-1])

success(f"HTB{(bitstring_to_bytes(bits).decode())}")
```