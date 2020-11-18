a = str(input('Enter the word to be checked  '))

list_1 = []
list_2 = []

for i in a:
    list_1.append(i)

list_3 = list_1

for i in list_3:
    list_2.append(list_1[-1])
    del list_1[-1]
if list_2 == list_3:
    print('Worked')
