import random as rand


def get_random():
    operations = ['add', 'sub', 'mul']
    operation_num_dict = {'add': range(10, 1000), 'sub': range(10, 1000), 'mul': range(2, 40)}
    operation = rand.choice(operations)
    return operation, operation_num_dict[operation]


def pick_numbers():
    operation, num_range = get_random()
    two_nums = [rand.choice(num_range) for i in range(2)]
    if operation == 'add':
        sol = two_nums[0] + two_nums[1]
    elif operation == 'sub':
        sol = two_nums.sort()[-1] - two_nums[0]
    elif operation == 'mul':
        sol = two_nums[0] * two_nums[1]
    return two_nums.sort(), operation, sol
print(pick_numbers())
