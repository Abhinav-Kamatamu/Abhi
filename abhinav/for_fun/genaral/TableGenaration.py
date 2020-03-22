import time

ask = input('Would you want to learn or test? [Yes, no]')
ask = ask.lower()
if ask == 'no':
    Table = int(input('Enter the table.  '))
    limit = int(input('Till where do you want to learn?  '))+ 1
    [print(f'{Table} X {i} = {Table * i}') for i in range(1, limit)]
else:
    enter = int(input('Set timer  '))
    print('start')
    time.sleep(enter)
    print('\nend')