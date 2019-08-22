import random

from poc_fifteen_template import Puzzle

def test_lower_row_invariant(puzzle, start):
    """ test lower row invariants """

    assert start[0] > 1, "not an interior tile"
    assert puzzle.lower_row_invariant(*start)
    
    if start[1] == 0:
        puzzle.solve_col0_tile(start[0])
    else:
        puzzle.solve_interior_tile(*start)

    if start[1] > 0:
        return puzzle.lower_row_invariant(start[0], start[1]-1)
    else:
        return puzzle.lower_row_invariant(start[0]-1, puzzle.get_width()-1)

def test_upper_row_invariants(puzzle, start):
    """ test row0 and row1 invariants """

    if start[0] == 1:
        assert puzzle.row1_invariant(start[1])
        puzzle.solve_row1_tile(start[1])
        return puzzle.row0_invariant(start[1])
    else:
        assert puzzle.row0_invariant(start[1])
        puzzle.solve_row0_tile(start[1])
        return puzzle.row1_invariant(start[1]-1)

def test_2x2(puzzle, dummy=None):
    """ test if puzzle's top-left corner is correct """
    
    assert puzzle.row1_invariant(1)
    puzzle.solve_2x2()
    #return puzzle.check_upper_left_corner()    
    return True

def test_game(puzzle, dummy=None):
    """ complete puzzle test runner """

    move_str = generate_random_move_str()
    valid_moves = []
    
    for move in move_str:
        try:
            puzzle.update_puzzle(move)
            valid_moves.append(move)
        except AssertionError:
            pass # ignore invalid moves
    
    print "puzzle string: %s\n" % "".join(valid_moves)
    print puzzle
    result = puzzle.solve_puzzle()
    
    return is_correct(puzzle)

def run_test(puzzle, start, name, complete=False, stats=[0,0]):
    """ run single test """
    print "running test '%s'" % name
    
    if complete:
        test_func = test_game
    else:       
        print puzzle
    
        if start is None:
            test_func = test_2x2
        else:
            test_func = test_lower_row_invariant if start[0] >= 2 else test_upper_row_invariants

    if test_func(puzzle, start):
        stats[0] += 1
        print puzzle
        print "test #%d: '%s' passed. total=%d/%d\n" % (sum(stats), name, stats[0], stats[1])
    else:
        stats[1] += 1
        print puzzle
        print "test #%d: '%s' failed. total=%d/%d\n" % (sum(stats), name, stats[0], stats[1])

def run_tests_interior():
    """ interior test runner """

    base = Puzzle(4, 5, [[10, 11, 12, 9, 8], 
                         [7, 6, 5, 4, 3], 
                         [2, 1, 0, 13, 14], 
                         [15, 16, 17, 18, 19]])

    obj = base.clone()
    run_test(obj, (2,2), "interior same col")

    obj = base.clone()
    obj.set_number(1,1, 12)
    obj.set_number(0,2, 6)
    run_test(obj, (2,2), "interior half left")

    obj = base.clone()
    obj.set_number(1,3, 12)
    obj.set_number(0,2, 4)
    run_test(obj, (2,2), "interior half right")

    obj = base.clone()
    obj.set_number(0,0, 12)
    obj.set_number(0,2, 10)
    run_test(obj, (2,2), "interior upper left")

    obj = base.clone()
    obj.set_number(0,4, 12)
    obj.set_number(0,2, 8)
    run_test(obj, (2,2), "interior upper right")

    obj = base.clone()
    obj.set_number(2,0, 12)
    obj.set_number(0,2, 2)
    run_test(obj, (2,2), "interior same row")

    obj = base.clone()
    obj.set_number(2,1, 12)
    obj.set_number(0,2, 1)
    run_test(obj, (2,2), "interior short path")

def run_tests_col0():
    """ column 0 test runner """

    base = Puzzle(4, 5, [[10, 6, 5, 4, 3], 
                          [2, 1, 8, 9, 7], 
                          [0, 11, 12, 13, 14], 
                          [15, 16, 17, 18, 19]])

    obj = base.clone()
    obj.set_number(1,0, 10)
    obj.set_number(0,0, 2)
    run_test(obj, (2,0), "col0 short path")

    obj = base.clone()
    run_test(obj, (2,0), "col0 upper left")

    obj = base.clone()
    obj.set_number(0,4, 10)
    obj.set_number(0,0, 3)
    run_test(obj, (2,0), "col0 upper right")

    obj = base.clone()
    obj.set_number(1,2, 10)
    obj.set_number(0,0, 8)
    run_test(obj, (2,0), "col0 half right")

    obj = base.clone()
    obj.set_number(1,1,  10)
    obj.set_number(0,0, 1)
    run_test(obj, (2,0), "col0 diagonal")

def run_tests_row1():
    """ row 1 test runner """

    base = Puzzle(4, 5, [[9, 4, 6, 5, 1], 
                         [7, 3, 8, 2, 0], 
                         [10, 11, 12, 13, 14],
                         [15, 16, 17, 18, 19]])

    obj = base.clone()
    run_test(obj, (1,4), "row1 upper left")

    base = Puzzle(4, 5, [[4,7,2,6,9],
                         [5,3,8,1,0],
                         [10,11,12,13,14],
                         [15,16,17,18,19]])
    obj = base.clone()
    run_test(obj, (1,4), "row1 upper right")
    
    obj = base.clone()
    obj.set_number(1,0, 9)
    obj.set_number(0,0, 7)
    run_test(obj, (1,4), "row1 lower left")

    obj = base.clone()
    obj.set_number(1,4, 9)
    obj.set_number(1,3, 0)
    obj.set_number(0,0, 2)
    obj.set_number(0,4, 4)
    obj.set_number(0,1, 1)
    run_test(obj, (1,3), "row1 lower half left")

    obj = base.clone()
    obj.set_number(1,4, 9)
    obj.set_number(1,3, 0)
    obj.set_number(1,2, 6)
    obj.set_number(0,2, 8)
    obj.set_number(0,4, 4)
    obj.set_number(0,1, 1)
    run_test(obj, (1,3), "row1 upper half left")
    
def run_tests_row0():
    """ row 0 test runner """

    base = Puzzle(4, 5, [[1, 5, 6, 0, 4], 
                         [7, 3, 2, 8, 9], 
                         [10, 11, 12, 13, 14],
                         [15, 16, 17, 18, 19]])

    obj = base.clone()
    run_test(obj, (0,3), "row0 lower half left")

    obj = base.clone()
    obj.set_number(0,1, 3)
    obj.set_number(1,1, 5)
    run_test(obj, (0,3), "row0 upper half left")

    obj = base.clone()
    obj.set_number(1,2, 3)
    obj.set_number(1,1, 2)
    run_test(obj, (0,3), "row0 diagonal")

    obj = base.clone()
    obj.set_number(1,0, 3)
    obj.set_number(1,1, 7)
    run_test(obj, (0,3), "row0 lower left")

    obj = base.clone()
    obj.set_number(0,0, 3)
    obj.set_number(1,1, 1)
    run_test(obj, (0,3),"row0 upper left")

    obj = Puzzle(4, 5, [[1, 2, 0, 3, 4], 
                        [6, 5, 7, 8, 9], 
                        [10, 11, 12, 13, 14], 
                        [15, 16, 17, 18, 19]])
    obj.solve_row0_tile(2)

def run_tests_2x2():
    """ 2x2 test runner """

    base = Puzzle(4, 5, [[1, 6, 2, 3, 4], 
                        [5, 0, 7, 8, 9], 
                        [10, 11, 12, 13, 14], 
                        [15, 16, 17, 18, 19]])

    obj = base.clone()
    run_test(obj, None, "2x2 #1")

    obj = base.clone()
    obj.set_number(0,0, 6)
    obj.set_number(0,1, 5)
    obj.set_number(1,0, 1)
    obj.set_number(1,1, 0)
    run_test(obj, None, "2x2 #2")
    
    base = Puzzle(3, 3, [[4, 3, 2], [1, 0, 5], [6, 7, 8]])
    
    obj = base.clone()
    run_test(obj, None, "2x2 #3")
    
def run_tests_game():
    """ complete game test runner """
    
    sizes = [(2,2), (2,3), (3,2), (3,3), (5,4), (2,5), (5,2)]
    
    for size in sizes:
        run_test(Puzzle(*size), None, "random Puzzle(%d,%d)" % size, True)

def is_correct(puzzle):
    for row in range(puzzle.get_height()):
        for col in range(puzzle.get_width()):
            if not puzzle.current_position(row, col) == (row, col):
                return False
    return True            
        
def generate_random_move_str():
    """ helper method to generate a random solvable puzzle """
    num = 100
    moves  = list("r" * 100 + "l" * 100 + "u" * 100 + "d" * 100)
    random.shuffle(moves)
    move_str = "".join(moves)

    return "".join(move_str)

run_tests_interior()
run_tests_col0()
run_tests_row1()
run_tests_row0()
run_tests_2x2()
run_tests_game()
