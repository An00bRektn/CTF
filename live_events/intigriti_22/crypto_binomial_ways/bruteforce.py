flagg = "27F;VPbAs>clu}={9ln=_o1{0n5tp~"
flag_length = len(flagg)

def factorial(n):
    f = 1
    for i in range(2, n+1):
        f *= i
    return f

def series(A, X, n):
    val = []
    nFact = factorial(n)
    for i in range(0, n + 1):
        niFact = factorial(n - i)
        iFact = factorial(i)
        aPow = pow(A, n - i)
        xPow = pow(X, i)
        val.append(int((nFact * aPow * xPow) / (niFact * iFact)))
    return val

def encrypt(flag):
    A = 1; X = 1; n = 30
    val = series(A, X, n)
    ct = []
    for i in range(len(flag)):
        ct.append(chr(ord(flag[i])+val[i]%26))
    return ''.join(ct)
    
if __name__ == "__main__":
    # Bruteforcing begins
    stuff = "1337UP{"
    chars = [chr(x) for x in range(33, 128)]
    i=0
    while True:
    	for c in chars:
    		tmp = stuff + c
    		encrypted = encrypt(tmp)
            # Weirdly enough, substrings don't work, not sure why
            # Taking the ascii value for each of the new chars worked though
    		if ord(encrypted[-1]) == ord(flagg[i+6]):
    			stuff += c
    			break

    	print(stuff)
    	i+=1
    	
