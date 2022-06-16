# Implementation of Recursive Affine Cipher in Python

# number of symbols in UTF-16 is 65536
# first symbol in unicode is \x00

import argparse
import re
from cryptomath import egcd, modinv
from pathlib import Path

# recursive affine cipher encryption function 
# returns the cipher text
def recursive_encrypt(text, alpha1, alpha2, beta1, beta2, power, first_symbol):

    '''

    y_i = (a_i*x_i + b_i) % power

    '''

    out = ''
    for t in text:
        out += chr((( alpha1*(ord(t) - ord(first_symbol)) + beta1 ) % power) + ord(first_symbol))
        alpha1, alpha2 = alpha2, (alpha1 * alpha2) % power
        beta1, beta2 = beta2, (beta1 + beta2) % power
    return out

# recursive affine cipher decryption function 
# returns original text
def recursive_decrypt(cipher, alpha1, alpha2, beta1, beta2, power, first_symbol):

    '''

    x_i = ((a_i)^-1*(y_i - b_i)) % power

    '''

    out = ''
    for c in cipher:
        out += chr((( modinv(alpha1, power)*(ord(c) - ord(first_symbol) - beta1 )) % power) + ord(first_symbol))
        alpha1, alpha2 = alpha2, (alpha1 * alpha2) % power
        beta1, beta2 = beta2, (beta1 + beta2) % power
    return out

# Driver Code to test the above functions
def main():

    parser=argparse.ArgumentParser(description="Recursive Affine Cipher")
    parser.add_argument('-i','--input',
                        help="For input paste string or path for the file"
                        "",required=True)
    parser.add_argument('-a1', '--alpha1',
                        help="Int A1. A1&B1 should be relatively prime numbers"
                        "",required=True, type=int)
    parser.add_argument('-a2', '--alpha2',
                        help="Int A2. A2&B2 should be relatively prime numbers"
                        "",required=True, type=int)
    parser.add_argument('-b1', '--beta1',
                        help="Int B1. A1&B1 should be relatively prime numbers"
                        "",required=True, type=int)
    parser.add_argument('-b2', '--beta2',
                        help="Int B2. A2&B2 should be relatively prime numbers"
                        "",required=True, type=int)
    args = parser.parse_args()


    # declaring text and alphas & betas
    alpha1 = args.alpha1
    alpha2 = args.alpha2
    beta1  = args.beta1
    beta2  = args.beta2

    try:
        with open(args.input) as file:
            text = file.read()
            recursive_encrypted_text = recursive_encrypt((re.sub('[^a-zA-Z]+', '', text)).upper(), alpha1, alpha2, beta1, beta2, 26, 'A').encode('utf-8', 'replace').decode()
            Path("output").mkdir(parents=True, exist_ok=True)
            with open('output/rec_enc_out.txt', 'w') as f:
                print(recursive_encrypted_text, file=f)
                print("Encrypted text in output/rec_enc_out.txt file")
            with open('output/rec_dec_out.txt', 'w') as f:
                print(recursive_decrypt(recursive_encrypted_text, alpha1, alpha2, beta1, beta2, 26, 'A'), file=f)
                print("Decrypted ciphertext in output/rec_dec_out.txt file")
    except:
        text = args.input
        recursive_encrypted_text = recursive_encrypt(text, alpha1, alpha2, beta1, beta2, 95, ' ').encode('utf-8', 'replace').decode()
        print('Recursive encrypted text: {}'.format( recursive_encrypted_text ))

        print('Recursive decrypted Text: {}'.format
              ( recursive_decrypt(recursive_encrypted_text, alpha1, alpha2, beta1, beta2, 95, ' ')))

if __name__ == '__main__':
    main()
