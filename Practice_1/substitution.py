# Implementation of Substitution Cipher in Python

import argparse
import random
import re
from pathlib import Path


def makeKey(alphabet):
    alphabet = list(alphabet)
    random.shuffle(alphabet)
    return ''.join(alphabet)

def encryptMessage(key, message, alphabet):
    return translateMessage(key, message, alphabet, 0)

def decryptMessage(key, message, alphabet):
    return translateMessage(key, message, alphabet, 1)

def translateMessage(key, message, alphabet, mode: bool):
    translated = ''
    charsA = alphabet
    charsB = key
    if mode == 1:
        # For decrypting, we can use the same code as encrypting. We
        # just need to swap where the key and LETTERS strings are used.
        charsA, charsB = charsB, charsA

    # loop through each symbol in the message
    for symbol in message:
        if symbol.upper() in charsA:
            # encrypt/decrypt the symbol
            symIndex = charsA.find(symbol.upper())
            if symbol.isupper():
                translated += charsB[symIndex].upper()
            else:
                translated += charsB[symIndex].lower()
        else:
            # symbol is not in LETTERS, just add it
            translated += symbol

    return translated

def main():

    parser=argparse.ArgumentParser(description="Substitution Cipher")
    parser.add_argument('-i','--input',
                        help="For input paste string or path for the file"
                        "",required=True)
    args = parser.parse_args()

    try:
        with open(args.input) as file:
            text = file.read()
            alphabet = ''.join(chr(i) for i in range(65,95))
            #alphabet = ''.join(chr(i) for i in range(32,127))
            key = makeKey(alphabet)
            print("Used key: {}".format(key))

            cipher = encryptMessage(key, text, alphabet)
            Path("output").mkdir(parents=True, exist_ok=True)
            with open('output/sub_enc_out.txt', 'w') as f:
                print(cipher, file=f)
                print("Encrypted text in output/sub_enc_out.txt file")
            with open('output/sub_dec_out.txt', 'w') as f:
                print(decryptMessage(key, cipher, alphabet), file=f)
                print("Decrypted ciphertext in output/sub_dec_out.txt file")
    except:
        text = args.input
        alphabet = ''.join(chr(i) for i in range(65, 95))
        key = makeKey(alphabet)

        cipher = encryptMessage(key, text, alphabet)
        print("Encrypted text: {}".format(cipher.encode('utf-8', 'replace').decode()))
        print("Decrypted ciphertext: {}".format(decryptMessage(key, cipher, alphabet)))

if __name__ == '__main__':
    main()
