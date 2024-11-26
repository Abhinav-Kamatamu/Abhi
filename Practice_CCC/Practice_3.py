# Refer to this link to find out the problmes:--    https://cemc.uwaterloo.ca/sites/default/files/documents/2024/2024CCCJrProblems.html

# Problem 3
'''

import random

how_many = [1, 0, 0]

data = [int(input()) for i in range(int(input()))]
# data = [random.randint(0,75) for i in range(250000)]

data.sort(reverse=True)
winner = [data[0], 0, 0]
turn = 0

for input in data:
    if input != winner[turn]:
        if turn == 2:
            break
        turn += 1
        winner[turn] = input
        how_many[turn] += 1
    else:
        how_many[turn] += 1

print(winner[2], how_many[2])
'''


def find_troublesome_keys(key_presses, screen_output):
    silly_key = None
    wrong_letter = None
    quiet_key = None

    # We will use dictionaries to track occurrences
    pressed = {}  # Dictionary to track characters that were pressed
    displayed = {}  # Dictionary to track characters that were displayed

    for key, display in zip(key_presses, screen_output):
        if key != display:  # Possible silly key
            if silly_key is None:
                silly_key = key
                wrong_letter = display
            elif key == silly_key and display == wrong_letter:
                continue  # Continue if we see the same mismatch
            else:
                # If different, this may indicate the wrong key setup, but not a concern in this task
                pass

        # Track the quiet key if no output is shown for a key
        if display == '-':
            if quiet_key is None and key != silly_key:
                quiet_key = key

    # Output the results
    print(silly_key, wrong_letter)
    if quiet_key:
        print(quiet_key)
    else:
        print('-')


# Sample Input 1
key_presses1 = "forloops"
screen_output1 = "fxrlxxps"
find_troublesome_keys(key_presses1, screen_output1)

# Sample Input 2
key_presses2 = "forloops"
screen_output2 = "fxrlxxp"
find_troublesome_keys(key_presses2, screen_output2)

# Sample Input 3
key_presses3 = "forloops"
screen_output3 = "frlpz"
find_troublesome_keys(key_presses3, screen_output3)

