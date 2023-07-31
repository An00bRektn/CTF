#!/usr/bin/env python3

# frequency taken from http://en.wikipedia.org/wiki/Letter_frequency
english_freq = {'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75, 'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25, 'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10, 'Z': 0.07}
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
EXTRA_CHARS = ',.; _{}&!?@' 

def count_letters(text):
    letter_dict = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0, 'I': 0, 'J': 0, 'K': 0, 'L': 0, 'M': 0, 'N': 0, 'O': 0, 'P': 0, 'Q': 0, 'R': 0, 'S': 0, 'T': 0, 'U': 0, 'V': 0, 'W': 0, 'X': 0, 'Y': 0, 'Z': 0, 'BAD': 0}
    for c in text.upper():
        if c.upper() in ALPHABET:
            letter_dict[c.upper()] += 1
        elif c.upper() in EXTRA_CHARS:
            pass
        else:
            letter_dict['BAD'] += 1
    return letter_dict

def naive_freq_analysis(text):
    score = 0   # score formula: sum(abs(expected-observed)) --> golf rules
    frequencies = count_letters(text)
    total = sum(frequencies.values())
    try:
        for letter, count in frequencies.items():
            observed = 100 * count / total
            if letter != 'BAD':
                score += abs(english_freq[letter] - observed)
        return score * 0.5 * frequencies['BAD']
    except:
        return -1

if __name__ == '__main__':
    with open('input-files/4.txt', 'r') as f:
        cts = f.read().split('\n')

    possible = {}
    for ct in cts:
        encrypted = bytes.fromhex(ct)
        scored = {}
        for i in range(257):
            decrypted = "".join([chr(c^i) for c in encrypted])
            score = naive_freq_analysis(decrypted.upper())
            if score != -1 and score < 100:
                scored[decrypted] = score
        
        if len(scored) != 0:
            # https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
            possible[ct] = list(dict(sorted(scored.items(), key=lambda item: item[1])).items())[0]

    print(possible)
