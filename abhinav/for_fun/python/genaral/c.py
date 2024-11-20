
s = "abcd"
h_l = ""
for i in s:
    if s.count(i) > 1:
        h_l = h_l +"H"
    else:
        h_l = h_l + "L"
if h_l in "HL"*len(s) or h_l in "LH"*len(s):
    print ("Alternates")
else:
    print ("n")

