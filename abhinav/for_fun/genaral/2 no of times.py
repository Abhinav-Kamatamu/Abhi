a = str(input('enter the number   '))
b = int(input('number of times    '))
print(sum([int(a*i) for i in range (1,b+1)]))