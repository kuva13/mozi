# Cryptanalysis Affine Cipher

import argparse
import detectEnglish, cryptomath, recursive_affine

demo_alpha1 = 7
demo_alpha2 = 11
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
    for key1 in range(demo_alpha1 * 95, 95 ** 2):
        for key2 in range(demo_alpha2 * 95, 95 ** 2):
            keyA1 = key1 // 95
            keyA2 = key2 // 95
            keyB1 = key1 % 95
            keyB2 = key2 % 95
            if (cryptomath.egcd(keyA1, 95)[0] == 1 and cryptomath.egcd(keyA2, 95)[0] == 1 and cryptomath.egcd(keyA1, keyA2)[0] == 1):

                decryptedText = recursive_affine.recursive_decrypt(message, keyA1, keyA2, keyB1, keyB2, 95, ' ')
                print('Tried Key pair A1: {:2d} A2: {:2d} B1: {:2d} B2: {:2d} Text: {:20s}'.format(keyA1, keyA2, keyB1, keyB2, decryptedText[:20]))

                if detectEnglish.isEnglish(decryptedText):
                    # Check with the user if the decrypted key has been found.
                    print('Possible encryption hack:')
                    print('Key pair A1: {} A2: {} B1: {} B2: {}'.format(keyA1, keyA2, keyB1, keyB2))
                    print('Decrypted message:')
                    print (decryptedText[:200])
                    print()
                    print('Enter D for done, or just press Enter to continue hacking:')
                    response = input('> ')

                    if response.strip().upper().startswith('D'):
                        return decryptedText

    return None

if __name__ == '__main__':
    main()
