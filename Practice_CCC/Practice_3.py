# Refer to this link to find out the problmes:--    https://cemc.uwaterloo.ca/sites/default/files/documents/2024/2024CCCJrProblems.html

#Problem 3
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
