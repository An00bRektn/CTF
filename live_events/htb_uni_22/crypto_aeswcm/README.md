# Brief Writeup

## Unintended
```python
def pad(self, pt):
    if len(pt) % self.BLOCK_SIZE != 0:
        pt = pad(pt, self.BLOCK_SIZE)
    return pt
```

Padding function bad - collision is possible just by entering nothing, and then the padding that would normally go on "Property: ".

## Intended
Quote aris in Discord
> the intended was to tag 3 times and the first tag would be the same as the third. 


