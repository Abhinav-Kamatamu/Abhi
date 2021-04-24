# --- while comparison for numbers ---
"""
operation = 0

while operation != 2:
    operation = int(input('Enter 1 for comparison and 2 to quit   '))

    if operation != 1 and operation != 2:
        print('That is not a valid operation \n try again')

    if operation == 1:
        i = int(input('Enter the number   '))
        a = int(input('Enter the number   '))

        if i > a:
            print(f'{i} is greater')
        elif i == a:
            print('they are equal')
        else:
            print(f'{a} is greater')
"""

# --- Bill Code ---
"""

operation = 0

while operation != 2:
    operation = int(input('Enter 1 to buy and 2 to quit   '))

    if operation != 1 and operation != 2:
        print('That is not a valid operation \n try again')

    if operation == 1:
        i = int(input('Enter the number of chocolates   '))
        bill = i * 10
        print('your bill is ', bill)
"""

# --- Series --- #
"""
first = int(input('What is the start of the series  '))
limit = int(input('Where do you want to end the code  '))
sum = 0
while first <= limit:
    print(first)
    sum += first
    first += 1
print(f'\n\nThe sum of all the numbers is {sum}')
"""

# --- Fibonacci series --- #

last = int(input('enter the number of fibonacci number you want   '))
previousTerm = 1
fakeTerm = previousTerm
term = 1
print('\t',1)
count = 2
while count <= last:
    print('\t',term)
    count += 1
    fakeTerm = term
    term += previousTerm
    previousTerm = fakeTerm
