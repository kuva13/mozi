from vigenere_shortslogan import Encryption_Short_Slogan
def main():

    alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    startMessage = input("Write the message: ").upper()
    oneKey = input("Write the key: ").upper()
    ciphertext = startMessage
    for i in range(len(alphabet)-1):
        ciphertext = Encryption_Short_Slogan(ciphertext, alphabet, oneKey)
    print("Decrypted Text: {}".format(ciphertext))
if __name__ == '__main__':
    main()
