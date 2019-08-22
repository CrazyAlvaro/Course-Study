"""
Test suite for score in "Yahtzee"
"""

import poc_simpletest

def run_suite(score):
    """
    Some informal testing code for score
    """
    
    # create a TestSuite object
    suite = poc_simpletest.TestSuite()
    
    # test score on various inputs
    hand = tuple([])
    suite.run_test(score(hand), 0, "Test #1:")

    hand = tuple([4, 2])
    suite.run_test(score(hand), 4, "Test #2:")
    
    hand = tuple((1, 2, 2))
    suite.run_test(score(hand), 4, "Test #3:")

    hand = tuple((2, 1, 2))
    suite.run_test(score(hand), 4, "Test #4:")

    hand = tuple([6, 2, 3])
    suite.run_test(score(hand), 6, "Test #5:")

    suite.report_results()
    
    


