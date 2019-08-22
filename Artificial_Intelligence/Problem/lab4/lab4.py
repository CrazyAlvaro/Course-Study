from __future__ import division
from classify import *
import math

##
## CSP portion of lab 4.
##
from csp import BinaryConstraint, CSP, CSPState, Variable,\
    basic_constraint_checker, solve_csp_problem

def pruning_variable_domain(constraint, state, var_i, var_j, pruning_var):
    # pruning variable's domain
    vals = pruning_var.get_domain()
    for val in vals:
        if var_i == pruning_var:
            i_val = val
            j_val = var_j.get_assigned_value() if var_j.is_assigned() else var_j.get_domain()[0]
            passed = constraint.check(state, i_val, j_val)
        elif var_j == pruning_var:
            i_val = var_i.get_assigned_value() if var_i.is_assigned() else var_i.get_domain()[0]
            j_val = val
            passed = constraint.check(state, i_val, j_val)
        else:
            raise Exception, "either var_i or var_j is the pruning_var"

        # val failed on satisfying constraint
        if not passed:
            pruning_var.reduce_domain(val)


def checking_variable_constraints(state, variable):
    var_name = variable.get_name()
    # find all binary constraints that are associated with curr_var
    constraints= state.get_all_constraints()

    for cons in constraints:
        if cons.get_variable_i_name() == var_name:
            another_var = state.get_variable_by_name(cons.get_variable_j_name())
            pruning_variable_domain(cons, state, variable, another_var, another_var)
        elif cons.get_variable_j_name() == var_name:
            another_var = state.get_variable_by_name(cons.get_variable_i_name())
            pruning_variable_domain(cons, state, another_var, variable, another_var)
        else:
            continue    # not related constraint

        if another_var.domain_size() == 0:
            return False

    return True


# Implement basic forward checking on the CSPState see csp.py
def forward_checking(state, verbose=False):
    # Before running Forward checking we must ensure
    # that constraints are okay for this state.
    basic = basic_constraint_checker(state, verbose)
    if not basic:
        return False

    curr_var = state.get_current_variable()

    # Root node
    if curr_var == None:
        return True

    return checking_variable_constraints(state, curr_var)

# Now Implement forward checking + (constraint) propagation through
# singleton domains.
def forward_checking_prop_singleton(state, verbose=False):
    # Run forward checking first.
    fc_checker = forward_checking(state, verbose)
    if not fc_checker:
        return False

    # Add your propagate singleton logic here.
    singleton_vars = filter(lambda var: var.domain_size() == 1,state.get_all_variables())
    all_cons = state.get_all_constraints()
    visited_vars = []

    while len(singleton_vars) > 0:
        curr_var = singleton_vars.pop(0)
        visited_vars.append(curr_var)

        proceed = checking_variable_constraints(state, curr_var)

        if proceed:
            new_singleton_vars = filter(lambda var: var.domain_size() == 1, state.get_all_variables())
            filtered_new_singleton_vars = filter(lambda v: not v in visited_vars and not v in singleton_vars, new_singleton_vars)
            singleton_vars = singleton_vars + filtered_new_singleton_vars
        else:
            return False

    return True

## The code here are for the tester
## Do not change.
from moose_csp import moose_csp_problem
from map_coloring_csp import map_coloring_csp_problem

def csp_solver_tree(problem, checker):
    problem_func = globals()[problem]
    checker_func = globals()[checker]
    answer, search_tree = problem_func().solve(checker_func)
    return search_tree.tree_to_string(search_tree)

##
## CODE for the learning portion of lab 4.
##

### Data sets for the lab
## You will be classifying data from these sets.
senate_people = read_congress_data('S110.ord')
senate_votes = read_vote_data('S110desc.csv')

house_people = read_congress_data('H110.ord')
house_votes = read_vote_data('H110desc.csv')

last_senate_people = read_congress_data('S109.ord')
last_senate_votes = read_vote_data('S109desc.csv')

### Part 1: Nearest Neighbors
## An example of evaluating a nearest-neighbors classifier.
# NOTE: split senate_people into two groups
senate_group1, senate_group2 = crosscheck_groups(senate_people)
# print "vote info: ", vote_info(senate_votes[0])
# print "vote info: ", vote_info(senate_votes[1])
# print "vote info: ", vote_info(senate_votes[2])
# print "vote info: ", vote_info(senate_votes[3])
# print "vote info: ", vote_info(senate_votes[4])
# print "vote info: ", vote_info(senate_votes[5])
# print "\n", "Use hamming_distance"
evaluate(nearest_neighbors(hamming_distance, 5), senate_group1, senate_group2, verbose=0)

## Write the euclidean_distance function.
## This function should take two lists of integers and
## find the Euclidean distance between them.
## See 'hamming_distance()' in classify.py for an example that
## computes Hamming distances.

def euclidean_distance(list1, list2):
    assert isinstance(list1, list)
    assert isinstance(list2, list)

    dist = 0

    for item1, item2 in zip(list1, list2):
        dist += abs(item1 - item2)**2
    return dist**(0.5)

#Once you have implemented euclidean_distance, you can check the results:
# print "\n", "Use euclidean_distance"
evaluate(nearest_neighbors(euclidean_distance, 5), senate_group1, senate_group2, verbose=0)

## By changing the parameters you used, you can get a classifier factory that
## deals better with independents. Make a classifier that makes at most 3
## errors on the Senate.

my_classifier = nearest_neighbors(hamming_distance, 5)
# print "\n", "Change parameters"
evaluate(my_classifier, senate_group1, senate_group2, verbose=0)

### Part 2: ID Trees
# print "senate_people", senate_people[0]
# print CongressIDTree(senate_people, senate_votes, homogeneous_disorder)

def single_disorder(homo_num, total_num):
    if homo_num == 0:
        return 0

    return -1 * (homo_num/total_num) * math.log(homo_num/total_num, 2)

def calculate_party_disorder(party_list):
    ind_num = 0
    rep_num = 0
    dem_num = 0
    for party in party_list:
        if party == "Democrat":
            dem_num += 1
        elif party == "Republican":
            rep_num += 1
        elif party == "Independent":
            ind_num += 1
        else:
            raise Exception, "Unknown party type %s" % (party)

    total_num = len(party_list)
    disorder = single_disorder(dem_num, total_num) +\
        single_disorder(rep_num, total_num) + single_disorder(ind_num, total_num)

    return disorder

## Now write an information_disorder function to replace homogeneous_disorder,
## which should lead to simpler trees.
def information_disorder(yes, no):
    '''
    yes is the legislators match the vote_value,
    while no is the legislators' vote different from the vote_value
    '''
    yes_disorder = calculate_party_disorder(yes)
    no_disorder = calculate_party_disorder(no)
    total_num = len(yes) + len(no)
    # print "yes_disorder: %s no_disorder: %s" % (yes_disorder, no_disorder)
    average_disorder = yes_disorder * len(yes)/total_num + no_disorder * len(no)/total_num
    return average_disorder


# print "\n", "Use information_disorder to produce simpler tree"
# print CongressIDTree(senate_people, senate_votes, information_disorder)
# evaluate(idtree_maker(senate_votes, homogeneous_disorder), senate_group1, senate_group2, 1)
# evaluate(idtree_maker(senate_votes, information_disorder), senate_group1, senate_group2, 1)

## Now try it on the House of Representatives. However, do it over a data set
## that only includes the most recent n votes, to show that it is possible to
## classify politicians without ludicrous amounts of information.

def limited_house_classifier(house_people, house_votes, n, verbose = False):
    house_limited, house_limited_votes = limit_votes(house_people,
    house_votes, n)
    house_limited_group1, house_limited_group2 = crosscheck_groups(house_limited)

    if verbose:
        print "ID tree for first group:"
        print CongressIDTree(house_limited_group1, house_limited_votes,
                             information_disorder)
        print
        print "ID tree for second group:"
        print CongressIDTree(house_limited_group2, house_limited_votes,
                             information_disorder)
        print

    return evaluate(idtree_maker(house_limited_votes, information_disorder),
                    house_limited_group1, house_limited_group2)


## Find a value of n that classifies at least 430 representatives correctly.
## Hint: It's not 10.
N_1 = 550
rep_classified = limited_house_classifier(house_people, house_votes, N_1, True)

## Find a value of n that classifies at least 90 senators correctly.
N_2 = 67
senator_classified = limited_house_classifier(senate_people, senate_votes, N_2, True)

## Now, find a value of n that classifies at least 95 of last year's senators correctly.
N_3 = 23
old_senator_classified = limited_house_classifier(last_senate_people, last_senate_votes, N_3, True)


## The standard survey questions.
HOW_MANY_HOURS_THIS_PSET_TOOK = "30"
WHAT_I_FOUND_INTERESTING = "forward_checking, and building identication tree, know house_people are more diverse to predict"
WHAT_I_FOUND_BORING = "None"

# print information_disorder(["Democrat", "Democrat", "Democrat"], ["Republican", "Republican"])
# print information_disorder(["Democrat", "Republican"], ["Republican", "Democrat"])

## This function is used by the tester, please don't modify it!
def eval_test(eval_fn, group1, group2, verbose = 0):
    """ Find eval_fn in globals(), then execute evaluate() on it """
    # Only allow known-safe eval_fn's
    if eval_fn in [ 'my_classifier' ]:
        return evaluate(globals()[eval_fn], group1, group2, verbose)
    else:
        raise Exception, "Error: Tester tried to use an invalid evaluation function: '%s'" % eval_fn
