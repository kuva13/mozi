def Encryption_Short_Slogan(message, alphabet, key):
    text2 = ''
    length_alphabet = len(alphabet)
    length_key = len(key)
    c = 0
    for char in message:
        try:
            text2 += alphabet[(alphabet.index(char) + alphabet.index(key[c % length_key])) % length_alphabet]
        except:
            text2 += char
        c += 1
    return text2


def Decryption_Short_Slogan(cripto, alphabet, key):
    text2 = ''
    length_alphabet = len(alphabet)
    length_key = len(key)
    c = 0
    for char in cripto:
        try:
            text2 += alphabet[(alphabet.index(char) - alphabet.index(key[c % length_key])) % length_alphabet]
        except:
            text2 += char
        c += 1
    return text2

def main():
    alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    startMessage = input("Write the message: ").upper()
    oneKey = input("Write the key: ").upper()
    ciphertext = Encryption_Short_Slogan(startMessage, alphabet, oneKey)
    print("Encrypted Text: {}".format(ciphertext))
    print("Decrypted Text: {}".format(
        Decryption_Short_Slogan(ciphertext, alphabet, oneKey)))

if __name__ == '__main__':
    main()
