# Brief Writeup

## Description
> Author: @Gary#4657

`These bits are shapepshifting! I need some help getting them back to their original form. Someone told me this might be a Fibonacci LFSR. `

## Writeup - Brute Force

You can read about an LFSR [here](https://en.wikipedia.org/wiki/Linear-feedback_shift_register#Fibonacci_LFSRs), but the solution I used was brute force. The flag format is only constrained to the characters `[a-f0-9{}lg]` (I hope that regex is right), which isn't a lot. Since the LFSR is only operating on pairs of characters, the total number of possibilities to brute force is ~256 at most, which Python can breeze right through.

TL;DR: Guess every 2 characters, see if it lines up with the output, and if it does, we found a correct character.