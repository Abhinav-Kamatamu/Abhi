print("==========wrong============")
with open('wrong.pkl', 'rb') as f:
    wrong_data = pickle.load(f)
print(wrong_data)

print("==========complete============")

with open('complete.pkl', 'rb') as f:
    complete_data = pickle.load(f)

# Create a list of tuples sorted by index 1 i.e. value field
listofTuples = sorted(complete_data.items(), key=lambda x: x[1])
# Iterate over the sorted sequence
for elem in listofTuples:
    print(elem[0], " ::", elem[1])