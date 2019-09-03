"""
Monte Carlo Tic-Tac-Toe Player
"""
#from sys import maxint
import random
#import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# Change as desired
NTRIALS = 1    # Number of trials to run
MCMATCH = 1.0  # Score for squares played by the machine player
MCOTHER = 1.0  # Score for squares played by the other player
    
# Add your functions here.

# my original design
#function to add score( board_with_score, score_board)
#function to choose a move( board, score_board)
#function to start a game()
#function to judge a game( board ), return boolean
#function to calc score of a finished game( board)


# This function takes a current board and the next player to move. 
# The function should play a game starting with the given player 
# by making random moves, alternating between players. 
# The function should return when the game is over. 
# The modified board will contain the state of the game, 
# so the function does not return anything. 
# In other words, the function should modify the board input.
def mc_trial(board, player):
    """ take a board and the next player to move """
    
    while board.check_win() == None:
        emtpy_list = board.get_empty_squares()
        #squar = random.choice( emtpy_list )  # choose a random tuple 
        #board.move( squar[0], squar[1], player )
        row, col= random.choice( emtpy_list )  # choose a random tuple 
        board.move( row, col, player )
        player = provided.switch_player(player)              # switch player

def mc_update_scores(scores, board, player):
    """ 
    update the scores with completed board,
    which player the machine play
    """
    result = board.check_win()
    other_player = provided.switch_player(player)
    dim = board.get_dim() 
    factor = 1 if result == player else  -1

    # if import as something, need to declare
    if result == None or result == provided.DRAW:    # in progress or DRAW
        return 

    for row in range(dim):
        for col in range(dim):
            squar = board.square(row, col)
            if squar == player:
                scores[row][col] +=  factor*MCMATCH
            elif squar == other_player:
                scores[row][col] += -factor*MCOTHER
            else:
                pass        # EMPTY


def get_best_move(board, scores):
    """ 
    from empty squares randomly return maximum score position
    return as a tuple
    """
    dim = board.get_dim()
    max_score = None
    pos_list = list()
    for row in range(dim):
        for col in range(dim):
            if board.square(row,col) == provided.EMPTY:
                if max_score == None:
                    max_score = scores[row][col]
                    pos_list.append((row,col))
                    continue 

                if scores[row][col] > max_score:
                    #print max_score, row, col
                    max_score = scores[row][col]
                    pos_list = []
                    pos_list.append((row,col))
                elif scores[row][col] == max_score:
                    pos_list.append((row,col))
                else:
                    pass
    if len(pos_list) == 0:
        print "no empty square"
        return None

    return random.choice(pos_list)


def mc_move(board, player, trials):
    """ 
    for specific board, and next player to run
    repeat trials number to run and get a good move
    """
    dim = board.get_dim()
    scores = [[0 for _ in range(dim)] for _ in range(dim)]
    for _ in range(trials+10):
        temp_board = board.clone()
        mc_trial(temp_board, player)
        mc_update_scores(scores, temp_board, player)
        
    return get_best_move(board, scores)    

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

# provided.play_game(mc_move, NTRIALS, False)        
# poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)




###############################################################
#
#
# Test suite for individual functions
#
#
###############################################################
#import other_test_suit as test_ttt
#test_ttt.test_trial(mc_trial)
# print
#test_ttt.test_update_scores(mc_update_scores, MCMATCH, MCOTHER)
# print
#test_ttt.test_best_move(get_best_move)

###############################################################
#
#
# Test suite for individual functions
#
#
###############################################################
#import another_test_suit as tests
#
#tests.test_mc_trial(mc_trial)                                             # tests for mc_trial
#
#tests.test_mc_update_scores(mc_update_scores, MCMATCH, MCOTHER)           # tests for mc_update_scores
#
#tests.test_get_best_move(get_best_move)                                   # tests for get_best_move
#
#tests.test_mc_move(mc_move, NTRIALS)                                      # tests for mc_move



#print get_best_move(provided.TTTBoard(3, False, [[provided.EMPTY, provided.EMPTY, provided.EMPTY], [provided.EMPTY, provided.EMPTY, provided.EMPTY], [provided.EMPTY, provided.EMPTY, provided.EMPTY]]), [[1, 2, 3], [7, 8, 9], [4, 5, 6]])
