dictab = {-100: "", 0: 'zero', 1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five',
          6: 'six', 7: 'seven', 8: 'eight', 9: 'nine', 10: 'ten',
          11: 'eleven', 12: 'Twelve', 13: 'thirteen', 14: 'forteen', 15: 'fifteen', 16: 'sixteen',
          17: 'seventeen', 18: 'eighteen'
    , 19: 'nineteen', 20: 'twenty', 30: 'thirty', 40: 'forty', 50: 'fifty',
          60: 'sixty', 70: 'seventy', 80: "eighty"
    , 90: 'ninety', 100: 'hundred', 1000: 'thousand', 100000: 'lakh'
    , 10000000: 'crore'
          }


# print (dictab
def boo(n):
    num_tencrore = (n // 100000000)
    n = n % 100000000
    num_crore = (n // 10000000)
    n = n % 10000000
    num_tenlakh = (n // 1000000)
    n = n % 1000000
    num_lakh = (n // 100000)
    n = n % 100000
    num_tenthousand = (n // 10000)
    n = n % 10000
    num_thousand = (n // 1000)
    n = n % 1000
    num_hund = (n // 100)
    n = n % 100
    num_ten = (n // 10)
    n = n % 10
    out = ''
    # print(num_tencrore,num_crore,num_tenlakh,num_lakh,num_tenthousand,num_thousand, num_hund, num_ten, n)
    if (num_tencrore > 0):
        out = out + (dictab[num_tencrore * 10] + " ")
    if (num_crore > 0):
        out = out + (dictab[num_crore] + " crore ")
    if (num_tenlakh > 0):
        out = out + (dictab[num_tenlakh * 10] + " ")
    if (num_lakh > 0):
        out = out + (dictab[num_lakh] + " lakh ")
    if (num_tenthousand > 0):
        out = out + (dictab[num_tenthousand * 10] + " ")
    if (num_thousand > 0):
        out = out + (dictab[num_thousand] + " thousand ")
    if (num_hund > 0):
        out = out + (dictab[num_hund] + " hundred ")
    if (num_ten > 0):
        out = out + (dictab[num_ten * 10] + " ")
    if (n > 0):
        out = out + (dictab[n])
    return (out)


g = int(input('enter the number that is to be named :'))

result = boo(g)

print(result)
