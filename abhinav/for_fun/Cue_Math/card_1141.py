#limit = 200
#num = 2
#bl = []
#for i in range(1,limit+1):
#    for j in str(i):
#        bl.append(j)
#print(bl.count(str(num)))



#print("".join([str(i) for i in range(0,201)]).count('2') )

s = "India is my country"

bl = s.split()
bl.reverse()
print(' '.join(bl))

print(" ".join(reversed(s.split())))