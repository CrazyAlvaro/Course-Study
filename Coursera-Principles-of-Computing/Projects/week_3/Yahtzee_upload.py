"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    
    # Traverse a hand tuple
    max_value = max(hand)
    scores = [ 0 for _ in range(max_value) ] 
    for dice in hand:
        scores[dice-1] += dice

    # for lower part check if is:
    # three of a kind, four of a kind, full house, small straight, large straight etc.

    return max(scores) 


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value of the held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    outcomes = [num for num in range(1, num_die_sides + 1) ]
    all_sequence = gen_all_sequences(outcomes, num_free_dice)

    total_score = 0.0
    for hand in all_sequence:
        temp_hand = tuple( list(held_dice) + list(hand) )
        total_score = total_score + score(temp_hand)
    
    return total_score/len(all_sequence)


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """

    choices = set()

    sub_lists = [[]]
    for dice in hand:
        #print sub_lists
        #temp_lists = sub_lists[:]

        for item in sub_lists[:]:       #loop over a copy of list
            #print item
            new_item = item[:]          # copy each list in list of lists
            new_item.append(dice)
            sub_lists.append(new_item)
                 
        #print sub_lists, temp_lists
        #sub_lists = sub_lists + temp_lists 

    #print sub_lists
    for subset in sub_lists:
        choices.add( tuple(subset) )
    return choices 



def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    all_choices = gen_all_holds( hand )
    max_expect = 0
    max_choice = (0.0, ())
    for temp_hand in all_choices:
        temp_expect = expected_value(temp_hand, num_die_sides, len(hand) - len(temp_hand))
        if temp_expect > max_expect:
            max_expect = temp_expect
            max_choice = ( max_expect, temp_hand)
    #print max_choice 
    return max_choice


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    
    
run_example()

