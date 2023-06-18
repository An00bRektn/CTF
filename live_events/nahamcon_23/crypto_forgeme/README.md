# Crypto: ForgeMe

The forgeme challenges were all based around a hash length extension attack. Hashes like SHA-1 and MD5 are based on the [Merkle-Damgaard](https://en.wikipedia.org/wiki/Merkle%E2%80%93Damg%C3%A5rd_construction) construction, where they break the input into blocks, and the hash is the result of running the algorithm on each block. The logic behind hash length extension is just continuing algorithm by using the current hash as a seed for the initial state.

ForgeMe1 is the most basic form of this, so I didn't write a solve script and just used [`hash_extender`](https://github.com/iagox86/hash_extender).

ForgeMe2 had a random key prepended to the input, so there was a bit more scripting required there, so there's actually a solve script for that.