# Implementation of Affine Cipher in Python

# number of symbols in UTF-16 is 65536
# first symbol in unicode is \x00
# re - regular expression
import argparse
import re
from cryptomath import egcd, modinv
from pathlib import Path

# affine cipher encryption function 
# returns the cipher text
def affine_encrypt(text, key, power, first_symbol):

    '''

    C = (a*P + b) % power

    '''

    return ''.join([ chr((( key[0]*(ord(t) - ord(first_symbol)) + key[1] ) % power) 
                         + ord(first_symbol)) for t in text ])

# affine cipher decryption function 
# returns original text
def affine_decrypt(cipher, key, power, first_symbol):

    '''

    P = (a^-1 * (C - b)) % power

    '''

    return ''.join([ chr((( modinv(key[0], power)*(ord(c) - ord(first_symbol) - key[1])) 
                          % power) + ord(first_symbol)) for c in cipher ])


# Driver Code to test the above functions
def main():

    parser=argparse.ArgumentParser(description="Affine Cipher")
    parser.add_argument('-i','--input',
                        help="For input paste string or path for the file"
                        "",required=True)
    parser.add_argument('-a', '--alpha',
                        help="Int A. A&B should be relatively prime numbers"
                        "",required=True, type=int)
    parser.add_argument('-b', '--beta',
                        help="Int B. A&B should be relatively prime numbers"
                        "",required=True, type=int)
    args = parser.parse_args()

    a = args.alpha
    b = args.beta
    key = [a, b]

    try:
        with open(args.input) as file:
            text = file.read()
            #affine_encrypted_text = affine_encrypt((re.sub('[^a-zA-Z]+', '', text)).upper(), key, 26, 'A')
            affine_encrypted_text = affine_encrypt(text, key, 95, ' ')
            Path("output").mkdir(parents=True, exist_ok=True)
            with open('output/aff_enc_out.txt', 'w') as f:
                print(affine_encrypted_text, file=f)
                print("Encrypted text in output/aff_enc_out.txt file")
            with open('output/aff_dec_out.txt', 'w') as f:
                print(affine_decrypt(affine_encrypted_text, key, 95, ' '), file=f)
                print("Decrypted ciphertext in output/aff_dec_out.txt file")
    except:
        text = args.input
        affine_encrypted_text = affine_encrypt(text, key, 95, ' ')
        print('Encrypted Text: {}'.format( affine_encrypted_text ))
        print('Decrypted Text: {}'.format
              ( affine_decrypt(affine_encrypted_text, key, 95, ' ') ))

if __name__ == '__main__':
    main()
