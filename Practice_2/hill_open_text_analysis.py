from tracemalloc import start
import numpy, argparse
import sympy
from hill import to_matrix
from hill import to_number_sequence
from hill import from_number_sequence
from hill import to_dividable_length
from hill import hill_decrypt
from math import gcd
from hill import invert_key
import time
import dict_check
from contextlib import redirect_stdout


def invert_matrix(mat_key, alphabet):
    sym_matrix = sympy.Matrix(mat_key)
    power = len(alphabet)
    det = sym_matrix.det()
    inverted_matrix = pow(int(det) % power, -1, power) * \
        (det*sym_matrix.inv()) % power
    return numpy.asarray(inverted_matrix)


def get_possible_block_sizes(enc, aplhabet):
    i = 1
    sizes = []
    while i**2 <= len(enc):
        if len(enc) % i == 0:
            sizes.append(i)
        i += 1

    return sizes


def fetch_keys(plain, enc, alphabet):

    possible_sizes = get_possible_block_sizes(enc, alphabet)
    probable_keys = []
    for size in possible_sizes:
        cur_plain = to_dividable_length(plain, size)

        mat_plain = to_matrix(to_number_sequence(cur_plain, alphabet), size)
        mat_enc = to_matrix(to_number_sequence(enc, alphabet), size)
        # msg*key=enc; key=enc/msg=enc*msg^-1
        blocks_plain = []
        blocks_enc = []
        for i in range(size):

            plain_block = mat_plain.take(list(size*i+j for j in range(size)))
            enc_block = mat_enc.take(list(size*i+j for j in range(size)))
            blocks_plain.append(plain_block)
            blocks_enc.append(enc_block)

        blocks_plain = numpy.asarray(blocks_plain)
        blocks_enc = numpy.asarray(blocks_enc)

        if gcd((int(sympy.Matrix(blocks_plain).det())), len(alphabet)) > 1:
            continue

        blocks_plain_inv = invert_matrix(blocks_plain, alphabet)

        probable_key = numpy.dot(
            blocks_plain_inv, blocks_enc).astype(float).round()

        probable_keys.append(from_number_sequence(
            (probable_key.transpose()).reshape(-1, ).tolist(), alphabet))

    return probable_keys


def main():

    parser=argparse.ArgumentParser(description="Plaintext Cryptanalysis of Hill Cipher")
    parser.add_argument('-p','--planetext',
                        help="For input paste string or path for the file"
                        "",required=True)
    parser.add_argument('-c', '--ciphertext',
                        help="For input paste string or path for the file"
                        "",required=True)
    args = parser.parse_args()

    plain, enc = args.planetext, args.ciphertext
    alphabet = 'abcdefghijklmnopqrstuvwxyz ?.,;'
    #alphabet = ' abcdefghijklmnopqrstuvwxyz?.,;'

    #start_time = time.time()
    keys = fetch_keys(plain, enc, alphabet)
    #time_spent = time.time()-start_time
    #print(f'Spent {time_spent} ')
    print(f'Probable keys: {keys}')

    if len(keys) > 0:
        max_score = 0
        best_key = ''
        for key in keys:
            with redirect_stdout(None):
                try:
                    attemted_text = hill_decrypt(enc, key, alphabet)
                    score = dict_check.dict_check(attemted_text)
                    if score >= max_score:
                        max_score = score
                    best_key = key

                except:
                    continue

        print(
            f'The best key found is "{best_key}", which scored {max_score} on dictionary check.')
        # if max_score == 0:
        #     print(
        #         'Keys seem to have not decoded words. Perhaps, the cypher was used multiple times.')


if __name__ == '__main__':
    main()
