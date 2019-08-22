"""
Test suite for expected_value in "Yahtzee"
"""

import poc_simpletest

def run_suite(expected_value):
    """
    Some informal testing code for gen_all_holds
    """
    # create a TestSuite object
    suite = poc_simpletest.TestSuite()
    
    # test expected_value on various inputs
    held_dice =  ()
    num_die_sides = 6
    num_free_dice = 2
    suite.run_test(round(expected_value(held_dice, num_die_sides, num_free_dice), 7), round(5.0555556, 7), "Test #1:")
    
    
    held_dice =  (2, 1, 2)
    num_die_sides = 6
    num_free_dice = 3
    suite.run_test(round(expected_value(held_dice, num_die_sides, num_free_dice), 7), round(6.9120370, 7), "Test #2:")
    
    
    held_dice =  (2,)
    num_die_sides = 6
    num_free_dice = 5
    suite.run_test(round(expected_value(held_dice, num_die_sides, num_free_dice), 7), round(8.8801440, 7), "Test #3:")
    
    
    held_dice =  (1,)
    num_die_sides = 6
    num_free_dice = 2
    suite.run_test(round(expected_value(held_dice, num_die_sides, num_free_dice), 7), round(5.0833333, 7), "Test #4:")
    
    
    held_dice =  (2, 1)
    num_die_sides = 6
    num_free_dice = 3
    suite.run_test(round(expected_value(held_dice, num_die_sides, num_free_dice), 7), round(6.4722222, 7), "Test #5:")
    
    
    held_dice =  (2, 2)
    num_die_sides = 6
    num_free_dice = 5
    suite.run_test(round(expected_value(held_dice, num_die_sides, num_free_dice), 7), round(9.2250514, 7), "Test #6:")
    
    
    held_dice =  (1, 2)
    num_die_sides = 6
    num_free_dice = 4
    suite.run_test(round(expected_value(held_dice, num_die_sides, num_free_dice), 7), round(7.6689815, 7), "Test #7:")
    

    suite.report_results()
    
    


