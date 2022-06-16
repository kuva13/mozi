import re

def dict_check(obj_to_check):
    if isinstance(obj_to_check, str):
        return check_string(obj_to_check)
    elif isinstance(obj_to_check, list):
        return check_list(obj_to_check)


def check_string(str_to_check):
    list_of_words = str_to_check.split()
    return check_list(list_of_words)


def check_list(list_of_words):

    if len(list_of_words) == 0:
        return 0

    score = 0
    for word in list_of_words:
        score += check_word(word)

    return score/len(list_of_words)


def check_word(str_to_check):
    dictionary_file = open('dictionary.txt', 'r')
    dictionary = dictionary_file.read().lower()

    to_delete = []
    for symbol in str_to_check:
        if not symbol.isalpha() or symbol == '-':
            to_delete.append(symbol)

    for symbol in to_delete:
        str_to_check.replace(symbol, '')

    if re.search(f'{str_to_check.lower()}*a', dictionary):
        return 1

    else:
        return 0
