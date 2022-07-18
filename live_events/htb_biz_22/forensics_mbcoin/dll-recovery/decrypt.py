from pwn import xor
with open('www1.dll', 'rb') as filp:
    ct = filp.read()

key1 = "6iIgloMk5iRYAw7ZTWed0CrjuZ9wijyQDjKO9Ms0D8K0Z2H5MX6wyOKqFxlOm1XpjmYfaQXacA6"

with open('www1-clean.dll', 'wb') as filp:
    filp.write(xor(ct, key1))

##############################
with open('www4.dll', 'rb') as filp:
    ct4 = filp.read()

key4 = "6iIoNoMk5iRYAw7ZTWed0CrjuZ9wijyQDjPy9Ms0D8K0Z2H5MX6wyOKqFxlOm1GpjmYfaQXacA6"
with open('www4-clean.dll', 'wb') as filp:
    filp.write(xor(ct4, key4))