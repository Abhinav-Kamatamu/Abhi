# """Problem number 3"""
#
# list_of_strings = [str(input()) for inputings in range(int(input()))]
# largest_no = 0
# day = []
# for j in range(5):
#     count = 0
#     for i in range(len(list_of_strings)):
#         if list_of_strings[i][j] == 'Y':
#             count += 1
#     if count > largest_no:
#         largest_no = count
#         day = [j]
#     elif count == largest_no:
#         day.append(j)
# output_str = ','.join(str(i + 1) for i in day)
# print(output_str)

"""Problem number 4"""

no_of_coloumns = int(input())
data = [(''.join(str(input()).split())) for row in range(2)]
length = 0


def get_no_neighbours(row, updown, tile, end_tail_left, end_tail_right):
    count = 0
    if data[row][tile - 1] == '1' and not end_tail_left:
        count += 1
    try:
        if data[row][tile + 1] == '1' and not end_tail_right:
            count += 1
    except:
        pass
    if updown:
        if data[row - 1][tile] == '1':
            count += 1
    return count


for i in range(2):
    for tile in range(1, no_of_coloumns - 1):
        if data[i][tile] == '1':
            if tile % 2 == 1:
                length += 3 - get_no_neighbours(i, False, tile, False, False)
            if tile % 2 == 0:
                length += 3 - get_no_neighbours(i, True, tile, False, False)
    if data[i][0] == '1':
        length += 3 - get_no_neighbours(i, True, 0, True, False)
    if data[i][-1] == '1':
        if (no_of_coloumns - 1) % 2 == 1:
            length += 3 - get_no_neighbours(i, False, no_of_coloumns - 1, False, True)
        else:
            length += 3 - get_no_neighbours(i, True, no_of_coloumns - 1, False, True)

print(length)
