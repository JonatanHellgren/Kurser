# Scaffold for solution to DIT873 / DAT346, Programming task 3

def sublist(s_list):
    # Create the sublist function which uses generators in order to
    # identify all sub-lists with ascending order
    # from a given l_list
    # Your code below
    a = s_list[0]   
    sub_list = [a]
    for b in s_list[1:]:
        if a <= b:
            sub_list.append(b)
            a = b
        else:
            yield(sub_list)
            a = b
            sub_list = [a]
    return

def longest_common_list(s_list):
    # Create the longest_common_list function which returns the common longest sublist
    # in s_list and the reverse of s_list
    # Please use the list comprehension in this function
    # Your code below
    lists1 = []
    for it in sublist(s_list):
        lists1.append(it)

    lists2 = []
    for it in sublist(s_list[::-1]):
        lists2.append(it)

    common = [l1 for l1 in lists1 for l2 in lists2 if l1 == l2]
    list_len = [len(l) for l in common]
    longest_ind = list_len.index(max(list_len))

    return common[longest_ind]



# The following is called if you execute the script from the commandline
# e.g. with python Solution.py
if __name__ == "__main__":

    assert longest_common_list([1,1,2,3,0,0,3,4,5,7,1,3,2,1,1,2]) == [1,1, 2, 3]
