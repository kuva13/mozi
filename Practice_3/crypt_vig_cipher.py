from vigenere_cipherkey import *

def main():
    alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    startMessage = input("Write the message: ").upper()
    oneKey = input("Write the key: ").upper()
    ciphertext = startMessage
    for i in range(2*len(alphabet)-1):
        ciphertext = Encryption_Vigenere_Cipher_Text(ciphertext, alphabet, oneKey)
    print("Decrypted Text: {}".format(ciphertext))

if __name__ == '__main__':
    main()
