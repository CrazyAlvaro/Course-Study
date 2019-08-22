def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length
    """
    ans = set([()])
    for dummy_idx in range(length):
        temp = set()
        for seq in ans:
            for item in outcomes:
                new_seq = list(seq)
                new_seq.append(item)
                temp.add(tuple(new_seq))
        ans = temp
    return ans

"""
Functionto generate permutations of outcomes
Repetitionof outcomes not allowed
"""

def gen_permutations(outcomes, length):
    """
    Iterative function that generates set of permutations of
    outcomes of length num_trials
    No repeated outcomes allowed
    """
    
    
    # add code here
    ans = set({()})
    #ans = set([()])        both works, turn a list of tuple into set, or turn dict of tuple into set
    
    for idx in range(length):
        temp = set()        # create a temporary set
        for perm in ans:
            for item in outcomes:
                if item in perm:
                    continue
                else:
                    new_seq = list(perm)
                    new_seq.append(item)
                    temp.add(tuple(new_seq))
        ans = temp
    ans = list(ans)
    ans.sort()
    return ans



def run_example():
    
    # example for digits
    #outcome = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    outcome = ["Red", "Green", "Blue"]
    #outcome = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    length = 2
    permtutations = gen_permutations(outcome, length)
    print "Computed", len(permtutations), "permutations of length", str(length)
    print "Permutations were", permtutations
    
    

run_example()




##Final example for homework problem
#
#outcome= set(["a", "b", "c", "d", "e", "f"])
#
#permutations= gen_permutations(outcome, 4)
#permutation_list= list(permutations)
#permutation_list.sort()
#print
#print"Answer is", permutation_list[100]
#
