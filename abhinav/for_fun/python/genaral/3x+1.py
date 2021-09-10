num = 2**68
initial_num = 2**68
def Check1():
    global num, initial_num
    if num ==1:
        initial_num+= 1
        num = initial_num
        print(initial_num)

while True:
    if num%2 == 0:
        num = num//2
        Check1()
    if num%2 == 1:
        num = num*3+1
        Check1()