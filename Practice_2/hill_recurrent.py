from locale import currency
from sympy import Matrix
import numpy, argparse, re
from math import gcd
from pathlib import Path


def to_matrix(sequence, block_size):

    cols = block_size
    rows = len(sequence)//block_size
    matrix = numpy.ndarray(shape=(rows, cols))

    for i in range(rows):
        for j in range(block_size):
            matrix[i, j] = sequence[block_size*i+j]

    return matrix


def invert_key(mat_key, alphabet):
    sym_key = Matrix(mat_key)
    power = len(alphabet)
    det = sym_key.det()
    inverted_key = pow(int(det) % power, -1, power)*(det*sym_key.inv()) % power
    return inverted_key


def to_number_sequence(text: str, alphabet: str):
    res = []
    for letter in text:
        res.append(alphabet.index(letter))

    return res


def from_number_sequence(sequence, alphabet):
    res = ''
    for number in sequence:
        res += alphabet[int(number) % len(alphabet)]

    return res


def to_dividable_length(msg, block_size, default_symbol='a'):
    to_add =(block_size - len(msg) % block_size) % block_size 

    result_msg = msg
    for _ in range(to_add):
        result_msg += default_symbol

    return result_msg


def rec_hill_encrypt(msg, key1, key2, alphabet, default_symbol='a'):
    block_size = int((len(key1))**0.5)
    msg = to_dividable_length(msg, block_size, default_symbol)

    mat_key1 = to_matrix(to_number_sequence(key1, alphabet), block_size)
    mat_key2 = to_matrix(to_number_sequence(key2, alphabet), block_size)

    mat_msg = to_matrix(to_number_sequence(msg, alphabet), block_size)

    if gcd(int(Matrix(mat_key1).det()) % len(alphabet), len(alphabet)) > 1:
        raise ValueError(
            'The key1 value makes it relatively not prime with alphabet. Please, use another one.')

    if gcd(int(Matrix(mat_key2).det()) % len(alphabet), len(alphabet)) > 1:
        raise ValueError(
            'The key2 value makes it relatively not prime with alphabet. Please, use another one.')

    result_seq = []

    for i in range(len(msg)//block_size):
        if i == 0:
            cur_key = mat_key1
            prev = mat_key1
        elif i == 1:
            cur_key = mat_key2
            prev = mat_key1
        else:
            prev, cur_key = cur_key, numpy.asmatrix(
                (Matrix(numpy.dot(cur_key, prev)) % len(alphabet))).astype(float).round()

        cur_row = numpy.ndarray(shape=(block_size, 1), buffer=mat_msg[i])

        row_result = numpy.dot(cur_key, cur_row)

        row_result = row_result.reshape(1, block_size)

        for i in range(block_size):
            result_seq.append(row_result[0, i])

    encrypted = from_number_sequence(result_seq, alphabet)

    return encrypted


def rec_hill_decrypt(msg, key1, key2, alphabet, default_symbol='a'):
    block_size = int((len(key1))**0.5)

    if len(msg) % block_size != 0:
        print('Message seems to be wrong with given keys. Adding some symbols. Check your keys.')
        msg = to_dividable_length(msg, block_size, default_symbol)

    mat_key1 = to_matrix(to_number_sequence(key1, alphabet), block_size)
    mat_key2 = to_matrix(to_number_sequence(key2, alphabet), block_size)

    mat_msg = to_matrix(to_number_sequence(msg, alphabet), block_size)

    if gcd(int(Matrix(mat_key1).det()) % len(alphabet), len(alphabet)) > 1:
        raise ValueError(
            'The key1 value makes it relatively not prime with alphabet. Please, use another one.')

    if gcd(int(Matrix(mat_key2).det()) % len(alphabet), len(alphabet)) > 1:
        raise ValueError(
            'The key2 value makes it relatively not prime with alphabet. Please, use another one.')

    result_seq = []

    for i in range(len(msg)//block_size):
        if i == 0:
            cur_key = mat_key1
            prev = mat_key1
        elif i == 1:
            cur_key = mat_key2
            prev = mat_key1
        else:
            prev, cur_key = cur_key, numpy.asmatrix(
                (Matrix(numpy.dot(cur_key, prev)) % len(alphabet))).astype(float).round()
        cur_row = numpy.ndarray(shape=(block_size, 1), buffer=mat_msg[i])
        inverted_key = numpy.asmatrix(invert_key(
            cur_key, alphabet)).astype(float).round()
        row_result = numpy.dot(inverted_key, cur_row)

        row_result = row_result.reshape(1, block_size)

        for i in range(block_size):
            result_seq.append(row_result[0, i])
    encrypted = from_number_sequence(result_seq, alphabet)

    return encrypted


def main():

    parser=argparse.ArgumentParser(description="Recurrent Hill Cipher")
    parser.add_argument('-i','--input',
                        help="For input paste string or path for the file"
                        "",required=True)
    parser.add_argument('-k1', '--key1',
                        help="String key should be perfect square lens"
                        "",required=True)
    parser.add_argument('-k2', '--key2',
                        help="String key should be perfect square lens"
                        "",required=True)
    args = parser.parse_args()

    alphabet = 'abcdefghijklmnopqrstuvwxyz ?.'
    #alphabet = ' abcdefghijklmnopqrstuvwxyz?.,;'

    try:
        with open(args.input) as file:
            msg  = re.sub('[^a-zA-Z]+', '', file.read()).lower()
            key1 = re.sub('[^a-zA-Z]+', '', args.key1).lower()
            key2 = re.sub('[^a-zA-Z]+', '', args.key2).lower()

            if len(key1)**0.5 % 1 != 0 or len(key2)**0.5 % 1 != 0:
                print('key must be a perfect square. aborting.')
                exit(1)

            if len(key1) != len(key2):
                print('keys must be of the same length. aborting.')
                exit(1)

            if any(key1[i] not in alphabet for i in range(len(key1)))   \
                or any(msg[i]not in alphabet for i in range(len(msg)))  \
                or any(key2[i] not in alphabet for i in range(len(key2))):

                print('incomprehensible symbols. use english alphabet only. aborting.')
                exit(1)

            encrypted_text = rec_hill_encrypt(msg, key1, key2, alphabet)
            decrypted_text = rec_hill_decrypt(encrypted_text, key1, key2, alphabet)

            Path("output").mkdir(parents=True, exist_ok=True)
            with open('output/rec_hill_enc_out.txt', 'w') as f:
                print(encrypted_text, file=f)
                print("Encrypted text in output/rec_hill_enc_out.txt file")
            with open('output/rec_hill_dec_out.txt', 'w') as f:
                print(decrypted_text, file=f)
                print("Decrypted ciphertext in output/rec_hill_dec_out.txt file")

    except:
        msg  = re.sub('[^a-zA-Z]+', '', args.input).lower()
        key1 = re.sub('[^a-zA-Z]+', '', args.key1).lower()
        key2 = re.sub('[^a-zA-Z]+', '', args.key2).lower()

        if len(key1)**0.5 % 1 != 0 or len(key2)**0.5 % 1 != 0:
            print('key must be a perfect square. aborting.')
            exit(1)

        if len(key1) != len(key2):
            print('keys must be of the same length. aborting.')
            exit(1)

        if any(key1[i] not in alphabet for i in range(len(key1)))   \
            or any(msg[i]not in alphabet for i in range(len(msg)))  \
            or any(key2[i] not in alphabet for i in range(len(key2))):

            print('incomprehensible symbols. use english alphabet only. aborting.')
            exit(1)

        encrypted_text = rec_hill_encrypt(msg, key1, key2, alphabet)
        decrypted_text = rec_hill_decrypt(encrypted_text, key1, key2, alphabet)

        print('Encrypted Text: {}'.format( encrypted_text ))
        print('Decrypted Text: {}'.format( decrypted_text ))


if __name__ == '__main__':
    main()
