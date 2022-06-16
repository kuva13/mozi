def Encryption_Vigenere_Cipher_Text(message, alphabet, key):
    text2 = ''
    length_alphabet = len(alphabet)
    c = 0
    for char in message:
        try:
            char_cripto = alphabet[(alphabet.index(char) + alphabet.index(key[c])) % length_alphabet]
            text2 += char_cripto
            key += char_cripto
        except:
            text2 += char
        c += 1
    return text2


def Decryption_Vigenere_Cipher_Text(cripto, alphabet, key):
    text2 = ''
    length_alphabet = len(alphabet)
    c = 0
    key += cripto
    for char in cripto:
        try:
            text2 += alphabet[(alphabet.index(char) - alphabet.index(key[c])) % length_alphabet]
        except:
            text2 += char
        c += 1
    return text2

def main():
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    string = input("Write the message: ").upper()
    key = input("Write the key: ").upper()
    encrypted_text = Encryption_Vigenere_Cipher_Text(string,alphabet, key)
    print("Ciphertext : {}".format(encrypted_text))
    print("Decrypted Ciphertext: {}".format(Decryption_Vigenere_Cipher_Text(encrypted_text, alphabet, key)))

if __name__ == '__main__':
    main()
