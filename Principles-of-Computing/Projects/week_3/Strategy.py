"""
Test suite for strategy in "Yahtzee"
"""

import poc_simpletest

def run_suite(strategy):
    """
    Some informal testing code for strategy
    """
    # create a TestSuite object
    suite = poc_simpletest.TestSuite()
    
    # test strategy on various inputs
    num_die_sides =  5
    hand =  (1, 3, 5, 3, 3)
    suite.run_test(strategy(hand, num_die_sides), (10.24, (3, 3, 3)), "Test #1:")
    
    
    num_die_sides =  4
    hand =  (3, 3, 3, 3)
    suite.run_test(strategy(hand, num_die_sides), (12.0, (3, 3, 3, 3)), "Test #2:")
    
    
    num_die_sides =  4
    hand =  (3, 1, 4, 4, 4)
    suite.run_test(strategy(hand, num_die_sides), (14.0, (4, 4, 4)), "Test #3:")
    
    
    num_die_sides =  8
    hand =  (1, 8, 4, 8)
    suite.run_test(strategy(hand, num_die_sides), (18.0, (8, 8)), "Test #4:")
    
    
    num_die_sides =  4
    hand =  (3, 1, 1, 3, 2)
    suite.run_test(strategy(hand, num_die_sides), (8.53125, (3, 3)), "Test #5:")
    
    
    num_die_sides =  6
    hand =  (6, 5)
    suite.run_test(strategy(hand, num_die_sides), (7.0, (6,)), "Test #6:")
    
    
    num_die_sides =  8
    hand =  (1, 8, 8)
    suite.run_test(strategy(hand, num_die_sides), (17.0, (8, 8)), "Test #7:")
    

    suite.report_results()
    
    


