a = str(input("enter   "))
b = []
c = []
for i in a:
    b.append(i)
for i in range(1,len(b)+1):
    c.append(b[0 - i])
print(a == "".join(c))
