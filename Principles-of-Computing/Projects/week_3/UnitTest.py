"""
Test suite for gen_all_holds in "Yahtzee"
"""

import poc_simpletest

def run_score_suite(score):
    """
    Some informal testing code for score
    """
    
    # create a TestSuite object
    suite = poc_simpletest.TestSuite()
    
    # test gen_all_holds on various inputs
    hand = tuple([])
    suite.run_test(score(hand), 0, "score empty hand")

    hand = tuple([4, 2])
    suite.run_test(score(hand), 4, "Score single max value")
    
    hand = tuple((1, 1, 2))
    suite.run_test(score(hand), 2, "Score with two max values")

    hand = tuple((2, 2, 3))
    suite.run_test(score(hand), 4, "Score with max value that is a sum")

    suite.report_results()

def run_expected_value_suite(expected_value):
    """
    Some informal testing code for expected_value
    """
    
    # create a TestSuite object
    suite = poc_simpletest.TestSuite()
    
    # test gen_all_holds on various inputs
    hand = tuple([])
    suite.run_test(expected_value(tuple([]), 6, 0), 0.0, "expected_value none held, no free dice")

    hand = tuple([])
    suite.run_test(expected_value(tuple([]), 5, 1), 3.0, "expected_value none held, one free, 5 sided die")
    
    hand = tuple((1, 1, 2))
    suite.run_test(expected_value(tuple([1]), 1, 1), 2.0, "expected_value holding a 1 , one free, 1 sided die")

    hand = tuple((1, 1, 2))
    suite.run_test(expected_value(tuple([5]), 5, 1), 6.0, "expected_value holding a 5 , one free, 5 sided die")

    hand = tuple((1, 1, 2))
    suite.run_test(expected_value(tuple([2]), 5, 1), 3.6, "expected_value holding a 2 , one free, 5 sided die")
    
    hand = tuple((2, 2, 3))
    suite.run_test(expected_value(tuple([1, 2, 3, 4, 5 ]), 5, 1), 6.8, "expected_value, holding one of each side, one 5 sided die")

    hand = tuple((2, 2, 3))
    suite.run_test(expected_value(tuple([1, 1, 2]), 4, 1), 3.5, "expected_value, with several ways of scoring on a 4 sided die")

    suite.report_results()    
    
    
 
def run_gen_all_holds_suite(gen_all_holds):
    """
    Some informal testing code for gen_all_holds
    """
    
    suite = poc_simpletest.TestSuite()
    
    hand = tuple([])
    suite.run_test(gen_all_holds(hand), set([()]), "gen_all_holds #1: empty hand")

    hand = tuple([4, 2])
    suite.run_test(gen_all_holds(hand), set([(), (4,), (2,), (4, 2)]), "gen_all_holds #2: holding two values")
    
    hand = tuple((1, 2, 2))
    suite.run_test(gen_all_holds(hand), set([(), (1,), (2,), (1, 2), (2, 2), (1, 2, 2)]), "gen_all_holds #3: holding 2 cards, 2 values: 1 2 1")

    hand = tuple((2, 1, 2))
    suite.run_test(gen_all_holds(hand), set([(), (1,), (2,), (1, 2), (2, 1), (2, 2), (2, 1, 2)]), "gen_all_holds #4:holding 2 cards, 2 values: 2 1 1 ")

    hand = tuple([6, 2, 3])
    suite.run_test(gen_all_holds(hand),set([(), (6,), (2,), (6, 2), (3,), (6, 3), (2, 3), (6, 2, 3)]), "gen_all_holds #5: 3 cards, 3 values")

    suite.report_results()
    
    
def run_strategy_suite(strategy):
    """
    Some informal testing code for strategy
    """
    
    suite = poc_simpletest.TestSuite()
    
    hand = tuple([])
    sides=6
    suite.run_test(strategy(hand, sides)[0], 0.0, "strategy: empty hand")
    suite.run_test(strategy(hand, sides)[1], (), "strategy: empty hand")
    
    hand = tuple([1])
    sides=5  
    suite.run_test(strategy(hand, sides)[0], 3.0, "strategy: holding one low value card")
    suite.run_test(strategy(hand, sides)[1], (), "strategy: holding one low value card")    

    hand = tuple([5])
    sides=5  
    suite.run_test(strategy(hand, sides)[0], 5.0, "strategy: holding one high value card")
    suite.run_test(strategy(hand, sides)[1], (5,), "strategy: holding one high value card")    

    hand = tuple([5,5])
    sides=5  
    suite.run_test(strategy(hand, sides)[0], 10.0, "strategy: holding high  pair")
    suite.run_test(strategy(hand, sides)[1], (5,5), "strategy: holding high  pair")    

    hand = tuple([1,1])
    sides=5  
    suite.run_test(strategy(hand, sides)[0], 4.4, "strategy: holding low pair")
    suite.run_test(strategy(hand, sides)[1], (), "strategy: holding low pair")       
    
    hand = tuple([5,1])
    sides=5  
    suite.run_test(strategy(hand, sides)[0], 6.0, "strategy: holding high/low pair")
    suite.run_test(strategy(hand, sides)[1], (5,), "strategy: holding high/low pair")       

    
    hand = tuple([3, 3, 3])
    sides=5   
    suite.run_test(strategy(hand, sides)[0], 9.0, "strategy: holding mid-value triplet")
    suite.run_test(strategy(hand, sides)[1], (3,3,3), "strategy: holding mid-value triplet")
    
    
    suite.report_results()

