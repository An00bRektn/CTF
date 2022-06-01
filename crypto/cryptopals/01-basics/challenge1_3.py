#!/usr/bin/env python3

# frequency taken from http://en.wikipedia.org/wiki/Letter_frequency
englishLetterFreq = {'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75, 'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25, 'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10, 'Z': 0.07}
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def count_letters(text):
    letter_dict = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0, 'I': 0, 'J': 0, 'K': 0, 'L': 0, 'M': 0, 'N': 0, 'O': 0, 'P': 0, 'Q': 0, 'R': 0, 'S': 0, 'T': 0, 'U': 0, 'V': 0, 'W': 0, 'X': 0, 'Y': 0, 'Z': 0}
    for c in text.upper():
        if c.upper() in ALPHABET:
            letter_dict[c.upper()] += 1
    return letter_dict

def naive_freq_analysis(text):
    score = 0   # score formula: sum(abs(expected-observed)) --> golf rules
    frequencies = count_letters(text)
    total = sum(frequencies.values())
    try:
        for letter, count in frequencies.items():
            observed = 100 * count / total
            score += abs(englishLetterFreq[letter] - observed)
        return score
    except:
        return 9999999999999999999999999

if __name__ == '__main__':
    encrypted = bytes.fromhex('1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736')
    scored = {}
    for i in range(257):
        decrypted = "".join([chr(c^i) for c in encrypted])
        scored[decrypted] = naive_freq_analysis(decrypted.upper())

    # https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
    print(dict(sorted(scored.items(), key=lambda item: item[1])))
