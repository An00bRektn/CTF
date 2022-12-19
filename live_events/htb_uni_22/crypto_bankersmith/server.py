from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes, inverse, GCD
from secret import FLAG, KEY

WELCOME = """
************** Welcome to the Gringatts Bank. **************
*                                                          *
*                  Fortius Quo Fidelius                    *
*                                                          *
************************************************************
"""


class RSA():

    def __init__(self, key_length):
        self.e = 0x10001
        phi = 0
        prime_length = key_length // 2

        while GCD(self.e, phi) != 1:
            self.p, self.q = getPrime(prime_length), getPrime(prime_length)
            phi = (self.p - 1) * (self.q - 1)
            self.n = self.p * self.q

        self.d = inverse(self.e, phi)

    def encrypt(self, message):
        message = bytes_to_long(message)
        return pow(message, self.e, self.n)

    def decrypt(self, encrypted_message):
        message = pow(encrypted_message, self.d, self.n)
        return long_to_bytes(message)


class Bank:

    def __init__(self, rsa):
        self.options = "[1] Get public certificate.\n[2] Calculate Hint.\n[3] Unlock Vault.\n"
        self.shift = 256
        self.vaults = {
            f"vault_{i}": [b"passphrase", b"empty"]
            for i in range(100)
        }
        self.rsa = rsa

    def initializeVault(self, name, passphrase, data):
        self.vaults[name][0] = passphrase
        self.vaults[name][1] = data

    def calculateHint(self):
        return (self.rsa.p >> self.shift) << self.shift

    def enterVault(self, vault, passphrase):
        vault = self.vaults[vault]
        if passphrase.encode() == vault[0]:
            return vault[1].decode()
        else:
            print("\nFailed to open the vault!\n")
            exit(1)


if __name__ == "__main__":
    rsa = RSA(2048)
    bank = Bank(rsa)

    vault = "vault_68"
    passphrase = KEY
    bank.initializeVault(vault, passphrase, FLAG)

    encrypted_passphrase = rsa.encrypt(bank.vaults[vault][0])
    print(f"You managed to retrieve: {hex(encrypted_passphrase)[2:]}")
    print("\nNow you are ready to enter the bank.")
    print(WELCOME)

    while True:
        try:
            print("Hello, what would you like to do?\n")
            print(bank.options)
            option = int(input("> "))

            if option == 1:
                print(f"\n{bank.rsa.n}\n{bank.rsa.e}\n")
            elif option == 2:
                print(f"\n{bank.calculateHint()}\n")
            elif option == 3:
                vault = input("\nWhich vault would you like to open: ")
                passphrase = input("Enter the passphrase: ")
                print(f"\n{bank.enterVault(vault, passphrase)}\n")
            else:
                "Abort mission!"
                exit(1)
        except KeyboardInterrupt:
            print("Exiting")
            exit(1)
        except Exception as e:
            print(f"An error occurred while processing data: {e}")
            exit(1)
