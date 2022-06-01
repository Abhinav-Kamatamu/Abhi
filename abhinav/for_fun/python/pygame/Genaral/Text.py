# if u find this file, delete it

n = int(input("Enter a number:- "))


def check_prime(x):
    factors = []
    i = 1
    product = 1
    while product != x:
        product = 1
        while x % i == 0:
            factors.append(i)
            if i == 1:
                break
        i += 1
        if i > x:
            return factors
        for j in factors:
            product *= j
    return factors


print(check_prime(n))
