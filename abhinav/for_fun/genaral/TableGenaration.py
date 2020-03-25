import pygame, time
pygame.init()
ask = input('Would you want to learn, practice, test or special practice? [L, p , t, sp] ')
ask = ask.lower()
if ask == '' or ask == 'l':
    Table = int(input('Enter the table.  '))
    limit = int(input('Till where do you want to learn?  '))+ 1
    print("".join([(f'{Table} X {i} = {Table * i}\n') for i in range(1, limit)]))
elif ask == 't':
    enter = int(input('Set timer.  '))
    print('start')
    time.sleep(enter)
    print('\nend')
elif ask == "p":
    enter = int(input('Set timer  '))
    table = int(input('Enter the table.  '))
    limit = int(input('Till where do you want to learn?  '))+ 1
    start = pygame.time.get_ticks()
    checker = False
    for i in range(1,limit):
        if checker > 0:
            i -= checker
        ans = int(input(f'{table} X {i} = '))
        if ans != table*i:
            print('\nWRONG!!!\n')
            checker += 1
        end = pygame.time.get_ticks()
        if end - start > enter*1000:
            print('time up')
            break

else:
    table = int(input('Enter the table.  '))
    limit = int(input('Till where do you want to learn?  '))+ 1
    start = pygame.time.get_ticks()
    enter = 2 * limit
    checker = 0
    i = 1
    teller = 0
    while i != limit:
        if checker > 0:
            if i > 0:
                i -= 1
        ans = int(input(f'{table} X {i} = '))
        if ans != table*i:
            print('\nWRONG!!!\n')
            checker += 1
        else:
            checker = 0
        end = pygame.time.get_ticks()
        if end - start > enter*1000:
            teller = pygame.time.get_ticks()
        i += 1

    if teller - start <= enter* 1000:
        print('perfect timing')
    elif teller -start >= (enter* 1000) and teller -start-(enter *1000) > 2000:
        print('A little over the limit but fine.')
    elif teller -start >= enter*1000 and teller -start -(enter*1000)>4000:
        print('Need to improve')
