import random as rd
import datetime
import time
import pickle

start = time.time()


def print_outfiles(wrong_file, complete_file):
    if len(dict_wrong) > 0:
        print("==========wrong============")
        with open(wrong_file, 'rb') as f:
            wrong_data = pickle.load(f)

        # Create a list of tuples sorted by index 1 i.e. value field
        listofTuples = sorted(wrong_data.items(), key=lambda x: x[1], reverse=True)
        # Iterate over the sorted sequence
        for elem in listofTuples:
            print(elem[0], " ::", elem[1])
    else:
        print("==========WRONG============")
        print("\t No mistakes!!!")

    print("==========complete============")

    with open(complete_file, 'rb') as f:
        complete_data = pickle.load(f)

    # Create a list of tuples sorted by index 1 i.e. value field
    listofTuples = sorted(complete_data.items(), key=lambda x: x[1], reverse=True)
    # Iterate over the sorted sequence
    for elem in listofTuples:
        print(elem[0], " ::", elem[1])


wrong_filename = "wrong_file_" + str(start).split(".")[1] + ".pkl"
complete_filename = "complete_file_" + str(start).split(".")[1] + ".pkl"
# ===============================================================Changeables
number_of_questions = 70

tough_number_list = [6, 7, 8, 9, 12, 13, 14, 15, 16, 17, 18, 19]

number_list = rd.sample(tough_number_list, 7)
# ===============================================================/Changables
print(number_list)

list_pending = [tuple([i, j]) for i in number_list for j in tough_number_list]
list_pending = rd.sample(list_pending, number_of_questions)

dict_complete = {}
dict_wrong = {}

try:
    while len(list_pending) > 0:
        tup = rd.choice(list_pending)
        start_item = time.time()
        try:
            ans = int(input("{} x {} = ".format(tup[0], tup[1])))
        except:
            ans = int(input("{} x {} = ".format(tup[0], tup[1])))
        total_time = time.time() - start_item

        if ans == tup[0] * tup[1]:
            list_pending.remove(tup)
            dict_complete[tup] = total_time
            f = open(complete_filename, "wb")
            pickle.dump(dict_complete, f)
            f.close()

        else:
            list_pending.remove(tup)
            dict_wrong[tup] = total_time
            f = open(wrong_filename, "wb")
            pickle.dump(dict_wrong, f)
            f.close()
    # your code here
    print(time.process_time() - start)

    print("Total items were : ", number_of_questions)
    print("Total Wrongs : ", len(dict_wrong))
    print("Total Corrects :", len(dict_complete))
    print("Total time is : ")
    # your code here
    print(time.time() - start)
    print_outfiles(wrong_filename, complete_filename)

except:

    print("Total items were : ", number_of_questions)
    print("Total Wrongs : ", len(dict_wrong))
    print("Total Corrects :", len(dict_complete))
    print("Total time is : ")
    # your code here
    print(time.time() - start)
    print_outfiles(wrong_filename, complete_filename)
