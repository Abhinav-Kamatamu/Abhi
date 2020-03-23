import pygame, time
pygame.init()
ask = input('Would you want to learn, practice,test? [L, p , t] ')
ask = ask.lower()
if ask == '' or ask == 'l':
    Table = int(input('Enter the table.  '))
    limit = int(input('Till where do you want to learn?  '))+ 1
    [print(f'{Table} X {i} = {Table * i}') for i in range(1, limit)]
elif ask == 't':
    enter = int(input('Set timer  '))
    print('start')
    time.sleep(enter)
    print('\nend')
else:
    enter = int(input('Set timer  '))
    table = int(input('Enter the table.  '))
    limit = int(input('Till where do you want to learn?  '))+ 1
    start = pygame.time.get_ticks()
    for i in range(1,limit):
        ans = int(input(f'{table} X {i} = '))
        if ans != table*i:
            print('\nWRONG!!!\n')
            i -= 1
        end = pygame.time.get_ticks()
        if end - start > enter*1000:
            print('time up')
            break
    