# Transposition Cipher Encryption

from math import ceil

def encryptMessage(key, message):
    # Each string in ciphertext represents a column in the grid:
    ciphertext = [''] * key

    # Loop through each column in ciphertext:
    for column in range(key):
        currentIndex = column

        # Keep looping until currentIndex goes past the message length:
        while currentIndex < len(message):
            # Place the character at currentIndex in message at the
            # end of the current column in the ciphertext list:
            ciphertext[column] += message[currentIndex]

            # Move currentIndex over:
            currentIndex += key

    # Convert the ciphertext list into a single string value and return it:
    return ''.join(ciphertext)

def decryptMessage(key, message):
    # The transposition decrypt function will simulate the "columns" and
    # "rows" of the grid that the plaintext is written on by using a list
    # of strings. First, we need to calculate a few values.
    
    # The number of "columns" in our transposition grid:
    numOfColumns = ceil(len(message) / key)
    # The number of "rows" in our grid will need:
    numOfRows = key
    # The number of "shaded boxes" in the last "column" of the grid:
    numOfShadedBoxes = (numOfColumns * numOfRows) - len(message)
    
    # Each string in plaintext represents a column in the grid.
    plaintext = [''] * numOfColumns
    
    # The col and row variables point to where in the grid the next
    # character in the encrypted message will go.
    col = 0
    row = 0
    
    for symbol in message:
        plaintext[col] += symbol
        col += 1 # point to next column
    
        # If there are no more columns OR we're at a shaded box, go back to
        # the first column and the next row.
        if (col == numOfColumns) or (col == numOfColumns - 1 and row >= numOfRows - numOfShadedBoxes):
            col = 0
            row += 1
    
    return ''.join(plaintext)

def main():
    myMessage = 'Common sense is not so common. КИРИЛЛИЦА'
    myKey = 8

    ciphertext = encryptMessage(myKey, myMessage)
    plaintext = decryptMessage(myKey, ciphertext)

    # Print the encrypted string in ciphertext to the screen, with
    # a | ("pipe" character) after it in case there are spaces at
    # the end of the encrypted message:
    print('Ciphertext: {}'.format(ciphertext))
    print('Plaintext: {}'.format(plaintext))

# If transpositionEncrypt.py is run (instead of imported as a module) call
# the main() function:
if __name__ == '__main__':
    main()
