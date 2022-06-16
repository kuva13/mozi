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


def hill_encrypt(msg, key, alphabet, default_symbol='a'):
    block_size = int((len(key))**0.5)
    msg = to_dividable_length(msg, block_size, default_symbol)

    mat_key = to_matrix(to_number_sequence(key, alphabet), block_size)
    mat_msg = to_matrix(to_number_sequence(msg, alphabet), block_size)
    if gcd(int(Matrix(mat_key).det()) % len(alphabet), len(alphabet)) > 1:
        raise ValueError(
            'The key value makes it relatively not prime with alphabet. Please, use another one.')

    result_seq = []

    for i in range(len(msg)//block_size):
        cur_row = numpy.ndarray(shape=(block_size, 1), buffer=mat_msg[i])

        row_result = numpy.dot(mat_key, cur_row)

        row_result = row_result.reshape(1, block_size).astype(float).round()

        for i in range(block_size):
            result_seq.append(row_result[0, i])

    encrypted = from_number_sequence(result_seq, alphabet)

    return encrypted


def hill_decrypt(msg, key, alphabet, default_symbol='a'):
    block_size = int((len(key))**0.5)

    if len(msg) % block_size != 0:
        raise ValueError ('Wrong message for the given key. Are you sure the key is correct?')
        #msg = to_dividable_length(msg, block_size, default_symbol)

    pre_mat_key = to_matrix(to_number_sequence(key, alphabet), block_size)
    if gcd(int(Matrix(pre_mat_key).det()) % len(alphabet), len(alphabet)) > 1:
        raise ValueError(
            'The key value makes it relatively not prime with alphabet. Please, use another one.')

    mat_key = invert_key(pre_mat_key, alphabet)

    if gcd(int(Matrix(mat_key).det()) % len(alphabet), len(alphabet)) > 1:
        raise ValueError(
            'The key value makes it relatively not prime with alphabet. Please, use another one.')

    mat_msg = to_matrix(to_number_sequence(msg, alphabet), block_size)

    result_seq = []

    for i in range(len(msg)//block_size):
        cur_row = numpy.ndarray(shape=(block_size, 1), buffer=mat_msg[i])

        row_result = numpy.dot(mat_key, cur_row)

        row_result = row_result.reshape(1, block_size)

        for i in range(block_size):
            result_seq.append(row_result[0, i])

    decrypted = from_number_sequence(result_seq, alphabet)
    return decrypted


def main():

    parser=argparse.ArgumentParser(description="Hill Cipher")
    parser.add_argument('-i','--input',
                        help="For input paste string or path for the file"
                        "",required=True)
    parser.add_argument('-k', '--key',
                        help="String key should be perfect square lens"
                        "",required=True)
    args = parser.parse_args()

    alphabet = 'abcdefghijklmnopqrstuvwxyz ?.,;'
    #alphabet = ' abcdefghijklmnopqrstuvwxyz?.,;'
    try:
        with open(args.input) as file:
            msg = re.sub('[^a-zA-Z]+', '', file.read()).lower()
            key =re.sub('[^a-zA-Z]+', '', args.key).lower() 

            if len(key)**0.5 % 1 != 0:
                print('Key must be a perfect square. Aborting.')
                exit(1)

            if any(key[i] not in alphabet for i in range(len(key))) \
                or any(msg[i] not in alphabet for i in range(len(msg))):

                print('Incomprehensible symbols. Use english alphabet only. Aborting.')
                exit(1)

            hill_encrypted_text = hill_encrypt(msg, key, alphabet, ' ')
            hill_decrypted_text = hill_decrypt(hill_encrypted_text, key, alphabet, ' ')

            Path("output").mkdir(parents=True, exist_ok=True)
            with open('output/hill_enc_out.txt', 'w') as f:
                print(hill_encrypted_text, file=f)
                print("Encrypted text in output/hill_enc_out.txt file")
            with open('output/hill_dec_out.txt', 'w') as f:
                print(hill_decrypted_text, file=f)
                print("Decrypted ciphertext in output/hill_dec_out.txt file")

    except:
        msg = args.input.lower()
        key = args.key.lower()

        if len(key)**0.5 % 1 != 0:
            print('Key must be a perfect square. Aborting.')
            exit(1)

        if any(key[i] not in alphabet for i in range(len(key))) \
            or any(msg[i] not in alphabet for i in range(len(msg))):

            print('Incomprehensible symbols. Use english alphabet only. Aborting.')
            exit(1)

        hill_encrypted_text = hill_encrypt(msg, key, alphabet)
        hill_decrypted_text = hill_decrypt(hill_encrypted_text, key, alphabet) 

        print('Encrypted Text: {}'.format( hill_encrypted_text ))
        print('Decrypted Text: {}'.format( hill_decrypted_text ))


if __name__ == '__main__':
    main()
