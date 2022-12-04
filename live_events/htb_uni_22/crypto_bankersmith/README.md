# Brief Writeup

This is just a classic RSA challenge. We're given the usual `n` and `e` as a public key, but we're also given a hint:

```python
def calculateHint(self):
    return (self.rsa.p >> self.shift) << self.shift
```

This returns the value of `p`, but the bottom 256 bits have been zeroed out. We know most of `p`, so like the title suggests, we can leverage Coppersmith to find the missing 256 bits.

There are two main implementations that circulate when these types of challenges come up:
- [defund/coppersmith](https://github.com/defund/coppersmith)
- [mimoo/RSA-and-LLL-attacks](https://github.com/mimoo/RSA-and-LLL-attacks)

I used mimoo's, but you can use either. Just follow the README's and you should be fine, and if you don't know what something does, just try and see what you need to fix.

Excuse the gross intermixing of regular sage and pwntools, I'm still new to using sage :D