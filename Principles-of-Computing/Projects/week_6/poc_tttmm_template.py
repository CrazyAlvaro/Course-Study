"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as provided
#import unit_test
# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(60)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

#def get_min_score(board, player):
#    """
#    from the board, get each move's minimum score and return it
#    """
#    #print "calling get_min_score"
#    min_score = 2
#    empty_squares = board.get_empty_squares()
#    if len(empty_squares) == 0:
#        return SCORES[board.check_win()]
#
#    for square in empty_squares:
#        row, col = square[0], square[1]
#
#        temp_board = board.clone()
#        temp_board.move(row, col, player)
#
#        temp_score = get_min_score( temp_board, provided.switch_player(player))
#        if min_score > temp_score:
#            min_score = temp_score
#
#    return min_score
#
#
#def get_max_score(board, player):
#    """
#    from the board, get each move's maximum score and return it
#    """
#    print "calling get_max_score"
#    print board.__str__()
#    max_score = -2
#    empty_squares = board.get_empty_squares()
#    if len(empty_squares) == 0:
#        print "len is 0"
#        return SCORES[board.check_win()]
#
#    for square in empty_squares:
#        row, col = square[0], square[1]
#
#        temp_board = board.clone()
#        temp_board.move(row, col, player)
#
#        temp_score = get_max_score( temp_board, provided.switch_player(player))
#        if max_score < temp_score:
#            max_score = temp_score
#    
#    return max_score

def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    if board.check_win() != None: 
        return SCORES[board.check_win()], (-1,-1)

    empty_squares = board.get_empty_squares()
    
    # choose the move with minimum max-loss(score)
    desired_move = (-1, -1)

    # for X player, get the minimum score from children
    if player == provided.PLAYERX:
        max_score = -2              # 1 for PLAYERX win, we want to choose the maximum of all 
        for square in empty_squares:
            row, col = square[0], square[1]
            
            # get a clone board and make a move
            temp_board = board.clone()
            temp_board.move(row, col, player)
            
            # calling help recursive function get min score
            # Only get first return value 
            temp_score, _ = mm_move(temp_board, provided.switch_player(player))
            if max_score < temp_score :
                max_score = temp_score
                desired_move = (row, col)
        
        return max_score, desired_move 

    # for O player, get the maximum score from children
    if player == provided.PLAYERO:
        min_score = 2               # -1 for PLAYERO to win, we want to choose the minimum of all
        for square in empty_squares:
            row, col = square[0], square[1]
            
            # get a clone board and make a move
            temp_board = board.clone()
            temp_board.move(row, col, player)
           
            # Only get first return value 
            temp_score, _ = mm_move(temp_board, provided.switch_player(player))
            #print "O's temp_score", temp_score
            if min_score > temp_score:
                min_score = temp_score
                desired_move = (row, col)

        return min_score, desired_move

    # undefined player
    return 0, (-1, -1)

def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

# provided.play_game(move_wrapper, 1, False)        
# poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)
#unit_test.test_mm_move(mm_move)
