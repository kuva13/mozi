from time import time
from hill_recurrent import *
import dict_check
import numpy
import sympy
from hill_open_text_analysis import get_possible_block_sizes
from contextlib import redirect_stdout


def sort_by_key_used(plain_arr, enc_arr, alphabet):
    min_sizes = []
    for text in enc_arr:
        cur_sizes = (get_possible_block_sizes(text, alphabet))
        if len(cur_sizes) < len(min_sizes) or len(min_sizes) == 0:
            min_sizes = cur_sizes

    first_key_sorted = {}
    second_key_sorted = {}
    for size in min_sizes:

        first_key_plain = ''
        second_key_plain = ''
        first_key_enc = ''
        second_key_enc = ''
        for i in range(len(plain_arr)):
            plain = to_dividable_length(plain_arr[i], size)
            enc = enc_arr[i]

            plain_symbols_for_first_key = plain[:size]
            enc_symbols_for_first_key = enc[:size]

            plain_symbols_for_second_key = plain[size:2*size]
            enc_symbols_for_second_key = enc[size: 2*size]

            first_key_plain += plain_symbols_for_first_key
            second_key_plain += plain_symbols_for_second_key
            first_key_enc += enc_symbols_for_first_key
            second_key_enc += enc_symbols_for_second_key

        first_key_sorted[size] = (first_key_plain, first_key_enc)
        second_key_sorted[size] = (second_key_plain, second_key_enc)

    return first_key_sorted, second_key_sorted


def extract_keys(key_dict, alphabet):
    probable_keys = {}

    for size in key_dict.keys():
        text_pair = key_dict[size]

        blocks_plain = numpy.array(to_number_sequence(
            text_pair[0], alphabet)[:size**2]).reshape(size, size)
        blocks_enc = numpy.array(to_number_sequence(text_pair[1], alphabet)[
                                 :size**2]).reshape(size, size)

        if gcd((int(sympy.Matrix(blocks_plain).det())), len(alphabet)) > 1:
            continue

        blocks_plain_inv = invert_key(blocks_plain, alphabet)

        probable_key = numpy.dot(
            blocks_plain_inv, blocks_enc).astype(float).round()

        probable_keys[size] = (from_number_sequence(
            (probable_key.transpose()).reshape(-1, ).tolist(), alphabet))

    return probable_keys


def full_analytic(plain_arr, enc_arr, alphabet):

    first_key, second_key = sort_by_key_used(plain_arr, enc_arr, alphabet)

    possible_first_keys = extract_keys(first_key, alphabet)
    possible_second_keys = extract_keys(second_key, alphabet)

    print(f'Possible first keys: {list(possible_first_keys.values())}')
    print(f'Possible second keys: {list(possible_second_keys.values())}')

    sizes_present_in_both = set()
    sizes_present_in_both.update(possible_first_keys.keys())
    sizes_present_in_both.update(possible_second_keys.keys())

    max_score = 0
    for present_size in sizes_present_in_both:
        score = 0

        for enc in enc_arr:
            try:
                with redirect_stdout(None):
                    attempted_text = rec_hill_decrypt(
                        enc, possible_first_keys[present_size], possible_second_keys[present_size], alphabet)
                score += dict_check.dict_check(attempted_text)
            except:
                score=0
        score = score/len(enc_arr)
        if score >= max_score:
            max_score = score
        best_key = (possible_first_keys[present_size],
                    possible_second_keys[present_size])

    print(
        f'The best key found is {best_key}')

    if max_score == 0:
        print('Keys seem to have not decoded words. Perhaps, the cypher was used multiple times.')


def main():
    plain = 'default'
    plain_arr = []
    enc_arr = []
    plain = input('Plain text(Type | for next text): ')
    enc = input('Encryption text(Type | for next text): ')
    plain_arr = plain.split('|')
    enc_arr = enc.split('|')
    #while plain != '':
    #    plain = input('Plain text(Press enter to abort): ')
    #    if plain == '':
    #        break
    #    enc = input('Encryption text: ')
    #    plain_arr.append(plain)
    #    enc_arr.append(enc)

    print('\n')
    alphabet = 'abcdefghijklmnopqrstuvwxyz ?.'

    full_analytic(plain_arr, enc_arr, alphabet)
if __name__ == '__main__':
    main()
