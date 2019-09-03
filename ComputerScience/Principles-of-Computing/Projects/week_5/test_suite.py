import poc_simpletest as test
import poc_wrangler_template as mod
# for example user34_ZLoVB9eL2zvE2cU

def remove_duplicates_test(function):

    suite = test.TestSuite()

    arr1 = [1, 1, 1, 1, 1, 1]
    arr2 = [1, 2, 3, 4, 5, 6]
    arr3 = [1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 4]
    arr4 = [-2, -2, -1, -1, 1, 2, 3, 3, 3, 4, 5]
    arr5 = [1]
    arr6 = []

    exp1 = [1]
    exp2 = [1, 2, 3, 4, 5, 6]
    exp3 = [1, 2, 3, 4]
    exp4 = [-2, -1, 1, 2, 3, 4, 5]
    exp5 = [1]
    exp6 = []

    suite.run_test(function(arr1), exp1, "Remove_dup #1")
    suite.run_test(function(arr2), exp2, "Remove_dup #2")
    suite.run_test(function(arr3), exp3, "Remove_dup #3")
    suite.run_test(function(arr4), exp4, "Remove_dup #4")
    suite.run_test(function(arr5), exp5, "Remove_dup #5")
    suite.run_test(function(arr6), exp6, "Remove_dup #6")

    suite.report_results()


def intersect_test(function):

    suite = test.TestSuite()

    l1a = []
    l1b = []
    ex1 = []

    l2a = []
    l2b = [1, 2, 3]
    ex2 = []

    l3a = [1, 2, 3]
    l3b = []
    ex3 = []

    l4a = [1, 2, 3, 4]
    l4b = [5, 6, 7, 8]
    ex4 = []

    l5a = [1, 2, 3, 4]
    l5b = [1, 2, 3, 4]
    ex5 = [1, 2, 3, 4]

    l6a = [1, 2, 3]
    l6b = [2, 3, 4]
    ex6 = [2, 3]

    l7a = [1, 5, 8]
    l7b = [2, 5, 7]
    ex7 = [5]

    l8a = [1, 3, 5, 9]
    l8b = [2, 3, 8, 9, 11]
    ex8 = [3, 9]

    l9a = [1, 1, 1, 1]
    l9b = [1, 1, 1, 1]
    ex9 = [1, 1, 1, 1]

    l10a = [1, 2, 2, 3, 4]
    l10b = [2, 3, 3, 4, 4]
    ex10 = [2, 3, 4]

    suite.run_test(function(l1a, l1b), ex1, "Intersect #1")
    suite.run_test(function(l2a, l2b), ex2, "Intersect #2")
    suite.run_test(function(l3a, l3b), ex3, "Intersect #3")
    suite.run_test(function(l4a, l4b), ex4, "Intersect #4")
    suite.run_test(function(l5a, l5b), ex5, "Intersect #5")
    suite.run_test(function(l6a, l6b), ex6, "Intersect #6")
    suite.run_test(function(l7a, l7b), ex7, "Intersect #7")
    suite.run_test(function(l8a, l8b), ex8, "Intersect #8")
    suite.run_test(function(l9a, l9b), ex9, "Intersect #9")
    suite.run_test(function(l10a, l10b), ex10, "Intersect #10")

    suite.report_results()


def merge_test(function):

    suite = test.TestSuite()

    l1a = []
    l1b = []
    ex1 = []

    l2a = []
    l2b = [1, 2, 3]
    ex2 = [1, 2, 3]

    l3a = [1, 2, 3]
    l3b = []
    ex3 = [1, 2, 3]

    l4a = [1, 2, 4]
    l4b = [5, 6, 7, 8]
    ex4 = [1, 2, 4, 5, 6, 7, 8]

    l5a = [1, 2, 3, 4]
    l5b = [1, 2, 3, 4]
    ex5 = [1, 1, 2, 2, 3, 3, 4, 4]

    l6a = [1]
    l6b = [2, 3, 4]
    ex6 = [1, 2, 3, 4]

    l7a = [1, 5, 8]
    l7b = [2, 5, 7]
    ex7 = [1, 2, 5, 5, 7, 8]

    l8a = [1, 3, 5, 9]
    l8b = [2, 3, 8, 9, 11]
    ex8 = [1, 2, 3, 3, 5, 8, 9, 9, 11]

    l9a = [1, 1, 1, 1]
    l9b = [1, 1]
    ex9 = [1, 1, 1, 1, 1, 1]

    l10a = [1, 2, 3, 4]
    l10b = [2, 3, 3, 4, 4]
    ex10 = [1, 2, 2, 3, 3, 3, 4, 4, 4]

    suite.run_test(function(l1a, l1b), ex1, "Merge #1")
    suite.run_test(function(l2a, l2b), ex2, "Merge #2")
    suite.run_test(function(l3a, l3b), ex3, "Merge #3")
    suite.run_test(function(l4a, l4b), ex4, "Merge #4")
    suite.run_test(function(l5a, l5b), ex5, "Merge #5")
    suite.run_test(function(l6a, l6b), ex6, "Merge #6")
    suite.run_test(function(l7a, l7b), ex7, "Merge #7")
    suite.run_test(function(l8a, l8b), ex8, "Merge #8")
    suite.run_test(function(l9a, l9b), ex9, "Merge #9")
    suite.run_test(function(l10a, l10b), ex10, "Merge #10")

    suite.report_results()


def merge_sort_test(function):

    suite = test.TestSuite()

    l1 = []
    e1 = []

    l2 = [1]
    e2 = [1]

    l3 = [1, 2, 3]
    e3 = [1, 2, 3]

    l4 = [1, 2, 3, 4]
    e4 = [1, 2, 3, 4]

    l5 = [5, 4, 3, 2, 1]
    e5 = [1, 2, 3, 4, 5]

    l6 = [5, 4, 3, 2]
    e6 = [2, 3, 4, 5]

    l7 = [3, 1, 5, 1, 6, 2, 6, 1, 3]
    e7 = [1, 1, 1, 2, 3, 3, 5, 6, 6]

    l8 = [3, 1, 5, 1, 6, 2, 6, 3]
    e8 = [1, 1, 2, 3, 3, 5, 6, 6]

    l9 = [1, 1, 1, 1]
    e9 = [1, 1, 1, 1]

    l10 = [1, 1, 1, 1, 1]
    e10 = [1, 1, 1, 1, 1]

    suite.run_test(function(l1), e1, "MergeSort #1")
    suite.run_test(function(l2), e2, "MergeSort #2")
    suite.run_test(function(l3), e3, "MergeSort #3")
    suite.run_test(function(l4), e4, "MergeSort #4")
    suite.run_test(function(l5), e5, "MergeSort #5")
    suite.run_test(function(l6), e6, "MergeSort #6")
    suite.run_test(function(l7), e7, "MergeSort #7")
    suite.run_test(function(l8), e8, "MergeSort #8")
    suite.run_test(function(l9), e9, "MergeSort #9")
    suite.run_test(function(l10), e10, "MergeSort #10")

    suite.report_results()


def gen_all_strings_test(function):

    suite = test.TestSuite()

    s1 = ""
    e1 = [""]

    s2 = "a"
    e2 = ["", "a"]

    s3 = "aa"
    e3 = ["", "a", "a", "aa", "aa"]

    s4 = "ab"
    e4 = ["", "b", "a", "ab", "ba"]

    s5 = "aab"
    e5 = ["", "b", "a", "ab", "ba", "a", "ab", "ba", "aa", "aa", "aab", "aab", "aba", "aba", "baa", "baa"]

    s6 = "baa"
    e6 = ["", "a", "a", "aa", "aa", "b", "ba", "ab", "ba", "ab", "baa", "aba", "aab", "baa", "aba", "aab"]

    s7 = "aba"
    e7 = ["", "a", "b", "ba", "ab", "a", "aa", "aa", "ab", "ba", "aba", "baa", "baa", "aab", "aab", "aba"]

    suite.run_test(function(s1), e1, "GenAllStrings #1")
    suite.run_test(function(s2), e2, "GenAllStrings #2")
    suite.run_test(function(s3), e3, "GenAllStrings #3")
    suite.run_test(function(s4), e4, "GenAllStrings #4")
    suite.run_test(function(s5), e5, "GenAllStrings #5")
    suite.run_test(function(s6), e6, "GenAllStrings #6")
    suite.run_test(function(s7), e7, "GenAllStrings #7")

    suite.report_results()


print "#################### REMOVE DUPLICATES ######################"
remove_duplicates_test(mod.remove_duplicates)
print "#############################################################"
print

print "######################## INTERSECT ##########################"
intersect_test(mod.intersect)
print "#############################################################"
print

print "########################## MERGE ############################"
merge_test(mod.merge)
print "#############################################################"
print

print "######################## MERGE SORT #########################"
merge_sort_test(mod.merge_sort)
print "#############################################################"
print

print "###################### GEN ALL STRINGS ######################"
print "### For this test suite (gen_all_strings) output may be   ###"
print "### in different order than expected. It means that even  ###"
print "### though failures are reported, your list can contain   ###"
print "### proper answers. To be sure compare your output        ###"
print "### precisely to that expected by failed tests (for       ###"
print "### example via a local sort of output lists).            ###"
print "#############################################################"
gen_all_strings_test(mod.gen_all_strings)
print "#############################################################"
