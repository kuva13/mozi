import argparse
from collections import OrderedDict
from curses.ascii import ispunct

def sort_dict_by_value_reverse(indict):
    """
    Returns an OrderedDict that has been sorted on value.

    :param indict:  A dict representing ngram probabilities.
    :return: An OrderedDict, sorted in reverse (largest to smallest)
    """
    outdict = OrderedDict()

    indictsorted = sorted(indict, key=indict.__getitem__, reverse=True)

    for i in indictsorted:
        outdict[i] = indict[i]

    return outdict


def build_ngram_counts(inputtext=None, n=1, countspace=False, countpunctuation=False):
    """
    Builds the ngram counts for a piece of text.
    :param inputtext: The text to measure.
    :param n: The n in n-gram
    :param countspace: Count spaces as a valid character in n-grams.
    :param countpunctuation: Count punctuation as valid characters in n-grams (minus new lines!)
    :return: A sorted OrderedDict containing the n-grams and counts of n-grams.
    """
    if inputtext is None or n < 1:
        return None

    ngrams = dict()
    for c in range(len(inputtext)):
        if not (inputtext[c].isalpha() or
                (ispunct(inputtext[c]) and countpunctuation is True and inputtext[c] != '\n') or
                (inputtext[c] == ' ' and countspace is True)):
            continue

        i = 0
        ngram = ""
        while len(ngram) < n and c+i < len(inputtext):
            if (inputtext[c+i].isalpha() or
                (ispunct(inputtext[c+i]) and countpunctuation is True and inputtext[c+i] != '\n') or
                    (inputtext[c+i] == ' ' and countspace is True)):
                ngram += inputtext[c+i]
            i += 1

        if len(ngram) == n:
            if ngram in ngrams:
                ngrams[ngram] += 1
            else:
                ngrams[ngram] = 1

    return sort_dict_by_value_reverse(ngrams)

def main():
    parser = argparse.ArgumentParser(description='Calculates letter frequencies of given cipher text in a cipher file.')
    parser.add_argument('CipherFile',
                        help='The cipher file to analyze.')
    parser.add_argument("-s", "--spaces", action='store_true',
                        help="Counts spaces as a valid cipher character instead of ignoring them."
                             "", required=False)
    parser.add_argument("-p", "--punctuation", action='store_true',
                        help="Counts punctuation as valid cipher characters instead of ignoring them."
                             "", required=False)

    args = parser.parse_args()

    cipherfile = args.CipherFile

    with open(cipherfile, 'r') as cf:
        ciphertext = cf.read()

    cipherlettercounts = build_ngram_counts(ciphertext, 1, args.spaces, args.punctuation)

    print("Letter Frequency:")
    for c in cipherlettercounts:
        print("{0} = {1}".format(c, cipherlettercounts[c]/len(ciphertext)))
    print("")

if __name__ == '__main__':
    main()
