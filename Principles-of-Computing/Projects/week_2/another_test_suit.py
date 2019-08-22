import poc_simpletest

import poc_ttt_provided as provided

TESTSUITE = poc_simpletest.TestSuite()

class TestBoard(provided.TTTBoard):
    def copy(self):
        self._copy_board = [ row[0:] for row in self._board ]

    def mod_board(self):
        self._board[0] = [provided.PLAYERX]*self._dim
        self.copy()

    def is_modified(self):
        return(self._copy_board!=self._board)

    def check_players(self):
        players = reduce(lambda x,y: x.union(y), self._board, set())
        return(players.issuperset(set([provided.PLAYERO,provided.PLAYERX])))

    def get_board(self):
        return(self._board)
    
    def fill_board(self,player):
        for row in range(len(self._board)):
            self._board[row] = [player]*self._dim



def test_mc_trial(mc_trial):
    print("Testing mc_trial")
    print("."*20)
    # if game is finished mc_trial should return without modifying board

    test_board = TestBoard(3)
    test_board.mod_board()
    mc_trial(test_board,provided.PLAYERX)
    TESTSUITE.run_test(test_board.is_modified(), False, "Test 1: mc_trial: if game is finished, then board shouldn't be modified")

    # mc_trial modifies board
    test_board = TestBoard(3)
    test_board.copy()
    mc_trial(test_board,provided.PLAYERX)
    TESTSUITE.run_test(test_board.is_modified(), True, "Test 2: board should be modified")

    # mc_trial switches players
    TESTSUITE.run_test(test_board.check_players(), True, "Test 3: mc_trial should switch players")

    # mc_trial returns different results
    test_board = TestBoard(3)
    test_board2 = TestBoard(3)
    mc_trial(test_board, provided.PLAYERX)
    mc_trial(test_board2, provided.PLAYERX)
    TESTSUITE.run_test(test_board.get_board()!=test_board2.get_board(), True, "Test 4: mc_trial should be randomized")

    TESTSUITE.report_results()
    print

class TestBoard2(provided.TTTBoard):
    def check_win(self):
        return(provided.DRAW)

def test_mc_update_scores(mc_update_scores, mcmatch, mcother):
    TESTSUITE.total_tests = 0
    TESTSUITE.failures = 0
    print("Testing mc_update_scores")
    print("."*20)
    # if DRAW mc_update_scores should return scores unmodified
    test_board = TestBoard2(1)
    scores = [[0]]
    mc_update_scores(scores,test_board,provided.PLAYERX)
    TESTSUITE.run_test(scores, [[0]], "Test 1: mc_update_scores shouldn't modify scores if DRAW")

    # if player==winner mc_update_scores should increment all squares status of which is equal to player by MCMATCH
    test_board = TestBoard(3)
    test_board.fill_board(provided.PLAYERX)
    scores = [[0]*3 for _ in range(3)]
    mc_update_scores(scores, test_board, provided.PLAYERX)
    TESTSUITE.run_test(scores, [[mcmatch]*3 for _ in range(3)], "Test 2: mc_update_scores: if player wins, score of player's squares should be incremented by MCMATCH")

    # if player!=winner mc_update_scores should increment all squares status of which is equal to other player by MCOTHER
    mc_update_scores(scores, test_board, provided.PLAYERO)
    TESTSUITE.run_test(scores, [[mcmatch+mcother]*3 for _ in range(3)], "Test 3: mc_update_scores: if player != winner, score other player's squares should be incremented by MCOTHER")

    # mc_update_scores should increment scores of winner's squares and decrement scores of loser's
    board = [[provided.PLAYERO]*3,[provided.PLAYERO]*3, [provided.PLAYERO, provided.PLAYERX, provided.PLAYERX]]
    test_board = TestBoard(dim=3, board=board)
    scores = [[0]*3 for _ in range(3)]
    mc_update_scores(scores, test_board, provided.PLAYERO)
    TESTSUITE.run_test(scores, [[mcmatch]*3, [mcmatch]*3, [mcmatch, -mcother, -mcother]], "Test 4: mc_update_scores should increment scores of winner's squares and decrement scores of loser's")

    TESTSUITE.report_results()
    print
    
def test_get_best_move(get_best_move):
    TESTSUITE.total_tests = 0
    TESTSUITE.failures = 0
    print("Testing get_best_move")
    print("."*20)
    # check if get_best_move returns correct answer
    import random

    test_board = TestBoard(3)
    choices = []
    results = []
    for i in range(10):
        scores = [[0]*3 for _ in range(3)]
        row,col = random.randrange(3), random.randrange(3)
        scores[row][col] += 5
        choices += [(row,col)]
        result = get_best_move(test_board, scores)
        results += [result]

    TESTSUITE.run_test(choices==results, True, "Test 1: get_best_move returns not the best choice")

    # check that get_best_move is randomized
    scores = [[1]*3 for _ in range(3)]
    TESTSUITE.run_test(len(reduce(lambda x,y: x.union([y]),[get_best_move(test_board, scores) for _ in range(10)], set())) > 1, True, "Test 2: get_best_move should return randomized choice if score of several squares are equal")

    # check that get_best_move handles negative scores
    scores = [[-1]*3 for _ in range(3)]
    try:
        TESTSUITE.run_test(len(get_best_move(test_board,scores)), 2, "Test 3: get_best_move should handle negative scores" )
    except IndexError:
        print("Test 3: get_best_move throws error if all scores are negative")
        TESTSUITE.total_tests += 1
        TESTSUITE.failures += 1
        
    # check that get_best_move returns only empty squares
    x = provided.PLAYERX
    test_board = TestBoard(dim=2, board = [[x,x],[x,1]])
    scores = [[2,2],[2,-2]]
    TESTSUITE.run_test(get_best_move(test_board,scores), (1,1), "Test 4: get_best_move returns non-empty square, should return only empty")
    
    TESTSUITE.report_results()
    print
    
def test_mc_move(mc_move, trials):
    TESTSUITE.total_tests = 0
    TESTSUITE.failures = 0
    print("Testing mc_move")
    print("."*20)
    # mc_move should return valid move
    x,o = provided.PLAYERX, provided.PLAYERO
    board = [[1,x,1],[o,x,1],[o,1,1]]
    test_board = TestBoard(dim=3, board=board)
    TESTSUITE.run_test(mc_move(test_board,x,trials) in test_board.get_empty_squares(), True, "Test 1: mc_move should return valid move")

    # mc_move should return good moves
    best_moves= [(0,0),(2,1)]
    TESTSUITE.run_test(all([mc_move(test_board,x,trials) in best_moves for _ in range(10)]), True, "Test 2: mc_move doesn't always return optimal move, try to increase NTRIALS")

    TESTSUITE.report_results()
    print