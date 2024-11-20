"""Problem #1"""
#
# data = [int(input()) for i in range(int(input()))]
# count = 0
# N = len(data)
# for person in range(N // 2):
#     if data[person] == data[N // 2 + person]:
#         count += 1
# print(count * 2)

'''Problem 2'''


def return_list(string):
    dict = {}
    ouput = []
    for char in range(len(string)):
        if string[char] not in dict:
            dict[string[char]] = [False, char]
            ouput.append(0)
        elif not dict[string[char]][0]:
            ouput[dict[string[char]][1]] = 1
            dict[string[char]] = [True]
            ouput.append(1)
        else:
            ouput.append(1)
    return ouput


def check(list):
    first = list[0]
    second = list[1]
    for element in range(len(list)):
        if element % 2 == 0:
            if not list[element] == first:
                return 'F'
        else:
            if not list[element] == second:
                return 'F'
    return 'T'


data = [(check(return_list(str(input())))) for i in range(int((str(input())).split()[0]))]
for i in data:
    print(i)


"""Problem 3"""

2