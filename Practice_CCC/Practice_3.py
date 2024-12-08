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


#Problem 4
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

'''

#Problem 4 -- working version

'''
def is_valid_mapping(pressed_keys, displayed_letters, silly_key, wrong_letter, quiet_key):
    i = 0  # Pointer for pressed_keys
    j = 0  # Pointer for displayed_letters
    prev_key = None  # Previous key pressed

    while i < len(pressed_keys):
        current_key = pressed_keys[i]

        if current_key == silly_key:
            # Silly key should map to wrong_letter
            if j >= len(displayed_letters) or displayed_letters[j] != wrong_letter:
                return False
            # Check constraints
            if prev_key == quiet_key:
                return False
            prev_key = silly_key
            i += 1
            j += 1
        elif quiet_key and current_key == quiet_key:
            # Quiet key does not display anything
            # Check constraints
            if prev_key == silly_key:
                return False
            prev_key = quiet_key
            i += 1
            # j remains the same
        else:
            # Normal key should display itself
            if j >= len(displayed_letters) or displayed_letters[j] != current_key:
                return False
            # Check constraints
            if (prev_key == quiet_key and current_key == silly_key) or \
               (prev_key == silly_key and current_key == quiet_key):
                return False
            prev_key = current_key
            i += 1
            j += 1

    # After processing all pressed_keys, all displayed_letters should be consumed
    if j != len(displayed_letters):
        return False

    return True

def find_troublesome_keys(pressed_keys, displayed_letters):
    pressed_set = set(pressed_keys)
    displayed_set = set(displayed_letters)

    for silly_key in pressed_set:
        # Possible wrong letters are displayed letters that are not the silly_key itself
        possible_wrong_letters = displayed_set.copy()
        if silly_key in possible_wrong_letters:
            possible_wrong_letters.remove(silly_key)

        for wrong_letter in possible_wrong_letters:
            # Possible quiet keys are keys that are pressed but never displayed, excluding the silly key
            possible_quiet_keys = pressed_set - displayed_set - {silly_key}
            quiet_keys_to_consider = list(possible_quiet_keys) + [None]

            for quiet_key in quiet_keys_to_consider:
                if is_valid_mapping(pressed_keys, displayed_letters, silly_key, wrong_letter, quiet_key):
                    # Output the silly key and wrong letter
                    print(f"{silly_key} {wrong_letter}")
                    # Output the quiet key or '-' if none
                    if quiet_key is not None:
                        print(quiet_key)
                    else:
                        print("-")
                    return

    # If no valid mapping is found
    print("No solution found")

# Read input
pressed_keys = input().strip()
displayed_letters = input().strip()

# Find and print the troublesome keys
find_troublesome_keys(pressed_keys, displayed_letters)
'''


# Problem 5

def main():
    # Read R and C directly
    R, C = map(int, input().strip().split())

    # Read the grid
    grid = []
    for _ in range(R):
        row = list(map(int, input().strip().split()))
        # If your input is well-formed, row should already have C elements
        grid.append(row)

    # Read the starting position (S_r, S_c)
    S_r, S_c = map(int, input().strip().split())
    S_r -= 1  # Convert to 0-based
    S_c -= 1

    if grid[S_r][S_c] == 0:
        print(0)
        return

    # Mark visited and use BFS
    visited = [[False]*C for _ in range(R)]
    visited[S_r][S_c] = True
    total_pumpkins = grid[S_r][S_c]

    queue = [(S_r, S_c)]
    head = 0

    directions = [(-1,0),(1,0),(0,-1),(0,1)]

    while head < len(queue):
        r, c = queue[head]
        head += 1

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C:
                if grid[nr][nc] > 0 and not visited[nr][nc]:
                    visited[nr][nc] = True
                    total_pumpkins += grid[nr][nc]
                    queue.append((nr, nc))

    print(total_pumpkins)

if __name__ == "__main__":
    main()

