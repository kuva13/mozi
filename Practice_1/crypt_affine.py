# Cryptanalysis Affine Cipher

import argparse
import detectEnglish, cryptomath, affine_cipher

def main():
    parser=argparse.ArgumentParser(description="Cryptanalysis of Affine Cipher")
    parser.add_argument('-i','--input',
                        help="For input paste string or path for the file"
                        "",required=True)
    args = parser.parse_args()

    myMessage = args.input

    try:
        with open(args.input) as file:
            myMessage = file.read()
            hackedMessage = hackAffine(myMessage)
            with open('cry_aff.txt', 'w') as f:
                print(hackedMessage, file=f)
                print("Full encryption in cry_aff.txt")

    except:
        myMessage = args.input
        hackedMessage = hackAffine(myMessage)

    if hackedMessage == None:
        print('Failed to hack encryption.')

def hackAffine(message):

    # brute-force by looping through every possible key
    for key in range(95 ** 2):
        keyA = key // 95
        keyB = key % 95
        if cryptomath.egcd(keyA, 95)[0] != 1:
            continue

        key_arr = [keyA, keyB]
        decryptedText = affine_cipher.affine_decrypt(message, key_arr, 95, ' ')
        #print('Tried Key pair A: {:2d} B: {:2d} Text: {:20s}'.format(keyA, keyB, decryptedText[:20]))

        if detectEnglish.isEnglish(decryptedText):
            # Check with the user if the decrypted key has been found.
            print('Possible encryption hack:')
            print('Key pair A: {} B: {}'.format(keyA, keyB))
            print('Decrypted message:')
            print (decryptedText[:200])
            print()

            return decryptedText
    return None

if __name__ == '__main__':
    main()
