number_of_digits = 10
currunt_num = 1
previous_num = 0
extra_num = 1

for i in range(1, number_of_digits):
    print(currunt_num)
    currunt_num += previous_num
    previous_num += extra_num
    extra_num = previous_num
