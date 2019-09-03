"""
Test Suite for methods in MiniMax Tic-Tac-Toe
"""
import poc_simpletest
from poc_ttt_provided import *

def test_mm_move(mm_move):
    """
    Test the mm_move function based on test cases from
    the OwlTest suite.
    """
    # Create a testSuite object
    suite = poc_simpletest.TestSuite()

    #[-25.0 pts] mm_move(TTTBoard(3, False, [[PLAYERX, EMPTY, EMPTY], [PLAYERO, PLAYERO, EMPTY], [EMPTY, PLAYERX, EMPTY]]), PLAYERX) returned bad move (-1, (2, 2))
    #[-12.0 pts] mm_move(TTTBoard(3, False, [[EMPTY, EMPTY, PLAYERX], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]), PLAYERO) expected score 0 but received (1, (2, 2))
    #[-30.0 pts] mm_move(TTTBoard(3, False, [[PLAYERX, PLAYERX, PLAYERO], [EMPTY, PLAYERX, PLAYERX], [PLAYERO, EMPTY, PLAYERO]]), PLAYERO) returned bad move (0, (-1, -1))
    #[-30.0 pts] mm_move(TTTBoard(2, False, [[EMPTY, EMPTY], [EMPTY, EMPTY]]), PLAYERX) expected score 1 but received (0, (-1, -1))
    #[-20.0 pts] mm_move(TTTBoard(3, False, [[PLAYERX, PLAYERX, PLAYERO], [PLAYERO, PLAYERX, PLAYERX], [PLAYERO, EMPTY, PLAYERO]]), PLAYERX) returned invalid move (0, (-1, -1))

    # Test 1
    board = TTTBoard(3, False, [[PLAYERX, EMPTY, EMPTY], [PLAYERO, PLAYERO, EMPTY], [EMPTY, PLAYERX, EMPTY]])
    expected = (0, (1, 2))
    move = mm_move(board, PLAYERX)
    suite.run_test(move, expected, "Test #1: X blocks O")

    # Test 2
    board = TTTBoard(3, False, [[EMPTY, EMPTY, PLAYERX], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]])
    expected = 0
    move = mm_move(board, PLAYERO)
    suite.run_test(move[0], expected, "Test #2: Tie game")
    
    # Test 3
    board = TTTBoard(3, False, [[PLAYERX, PLAYERX, PLAYERO], [EMPTY, PLAYERX, PLAYERX], [PLAYERO, EMPTY, PLAYERO]])
    expected = (-1, (2, 1))
    move = mm_move(board, PLAYERO)
    suite.run_test(move, expected, "Test #3: O chooses winning move")

    # Test 4
    board = TTTBoard(2, False, [[EMPTY, EMPTY], [EMPTY, EMPTY]])
    expected = 1
    move = mm_move(board, PLAYERX)
    suite.run_test(move[0], expected, "Test #4: X wins when going first on 2x2 board")

    # Test 5
    board = TTTBoard(3, False, [[PLAYERX, PLAYERX, PLAYERO], [PLAYERO, PLAYERX, PLAYERX], [PLAYERO, EMPTY, PLAYERO]])
    expected = (1, (2, 1))
    move = mm_move(board, PLAYERX)
    suite.run_test(move, expected, "Test #5: One square remaining on board")

    suite.report_results()
