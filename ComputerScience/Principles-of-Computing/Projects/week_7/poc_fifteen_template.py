"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

#import poc_fifteen_gui

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods
    def move_help(self, move_steps):
        """
        get move_steps string
        """
        for char in move_steps:
            self.update_puzzle(char)

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)

        # This assert would always being executed if not return before this
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        # Tile zero is positioned at (i,j)
        if self._grid[target_row][target_col]  != 0:
            return False

        # All tiles in rows i+1 or below are posistioned at their solved location
        for row in range(target_row + 1, self._height):
            for col in range(self._width):
                if self._grid[row][col] != (col + row*self._width):
                    return False
        
        # All tiles in row i to the right of position (i,j) are positioned at their solved location
        for col in range(target_col + 1, self._width):
            if self._grid[target_row][col] != (col + target_row*self._width):
                return False

        return True 

    def move_curr_to_target(self, curr_row, curr_col, target_row, target_col):
        """
        place curr_row, curr_col tile to target_row, target_col
        where zero tile current stay and set zero to target_row, target_col -1
        return the move string
        """
        assert self._grid[target_row][target_col] == 0, "zero not at target position"
        move_steps = ""
        # three cases: curr position is on up-left, up-right or up
        # move target to the up, then used left-hand cycle to move it down

        # straight move
        for _ in range(target_row - curr_row):
            move_steps += "u"
        for _ in range(target_col - curr_col):
            move_steps += "l"
        for _ in range(curr_col - target_col):
            move_steps += "r"

        # on the left side step of 0 
        if curr_col  < target_col:

            # for more than 1 step away from target_col
            for _ in range( target_col - curr_col - 1):
                if curr_row == 0:       # use lower right cycle
                    move_steps += "drrul"
                else:                   # use upper right cycle 
                    move_steps += "urrdl"

            # now at target's left side
            for _ in range( target_row - curr_row):
                move_steps += "druld"
            # done for left
        
        # straight up
        if curr_col == target_col:
            # for more than 1 step away from target_row
            for _ in range( target_row - curr_row -1):
                move_steps += "lddru"
            move_steps += "ld"
            # done for straight up

        if curr_col > target_col:
            # for more than 1 step away from target_col
            for _ in range( curr_col - target_col - 1):
                if curr_row == 0:       # use lower left cycle
                    move_steps += "dllur"
                else:                   # use upper left cycle
                    move_steps += "ulldr"
            if curr_row == 0:           # use lower left cycle
                move_steps += "dllu"
            else:                       # use upper left cycle
                move_steps += "ulld"
            # now at target's left side
            for _ in range( target_row - curr_row):
                move_steps += "druld"
            # done for right

        return move_steps

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        while i > 1 and j > 0
        """
        assert self.lower_row_invariant(target_row, target_col), "lower_row_invariant failed"
        curr_row, curr_col = self.current_position( target_row, target_col )
        move_steps = self.move_curr_to_target(curr_row, curr_col, target_row, target_col)
        
#        move_steps = ""
#        # three cases: target is on up-left, up-right or up
#        # move target to the up, then used left-hand cycle to move it down
#        
#        # get curr position
#        curr_row, curr_col = self.current_position( target_row, target_col )
#
#        # straight move
#        for _ in range(target_row - curr_row):
#            move_steps += "u"
#        for _ in range(target_col - curr_col):
#            move_steps += "l"
#        for _ in range(curr_col - target_col):
#            move_steps += "r"
#
#        # on the left side step of 0 
#        if curr_col  < target_col:
#
#            # for more than 1 step away from target_col
#            for _ in range( target_col - curr_col - 1):
#                if curr_row == 0:       # use lower right cycle
#                    move_steps += "drrul"
#                else:                   # use upper right cycle 
#                    move_steps += "urrdl"
#
#            # now at target's left side
#            for _ in range( target_row - curr_row):
#                move_steps += "druld"
#            # done for left
#        
#        # straight up
#        if curr_col == target_col:
#            # for more than 1 step away from target_row
#            for _ in range( target_row - curr_row):
#                move_steps += "lddrl"
#            move_steps += "ld"
#            # done for straight up
#
#        if curr_col > target_col:
#            # for more than 1 step away from target_col
#            for _ in range( curr_col - target_col - 1):
#                if curr_row == 0:       # use lower left cycle
#                    move_steps += "dllur"
#                else:                   # use upper left cycle
#                    move_steps += "ulldr"
#            move_steps += "ulld"
#            # now at target's left side
#            for _ in range( target_row - curr_row):
#                move_steps += "druld"
#            # done for right
        
        # make moves
        #print move_steps
        for char in move_steps:
            self.update_puzzle(char)

        return move_steps

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        assert self._grid[target_row][0] == 0, " zero not on target position"

        move_steps = ""
        # move zero up 
        self.update_puzzle("u")
        # It's possible that (target_row,0) is on upper 
        if self._grid[target_row][0] == target_row*self._width:
            move_steps = move_steps + "u"
            for _ in range(1, self._width):
                self.update_puzzle("r")
                move_steps = move_steps + "r"    
            return move_steps 

        # otherwise move zero right
        self.update_puzzle("r")


        # get curr position of tile target at (target_row, 0)
        curr_row, curr_col = self.current_position( target_row, 0)
        move_steps = self.move_curr_to_target(curr_row, curr_col, target_row-1, 1)
        # self._grid[target_row -1][0] == 0 after execute move_steps
        
        move_steps = move_steps + "ruldrdlurdluurddlu"

        # move to right most
        for _ in range(1, self._width):
            move_steps = move_steps + "r"

        self.move_help(move_steps) 
        #for char in move_steps:
        #    self.update_puzzle(char)
        
        # initially move up right
        return "ur" + move_steps

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        if self._grid[0][target_col] != 0:
            return False

        for row in range( 2, self._height):
            for col in range( self._width):
                if self._grid[row][col] != (col + row*self._width):
                    return False 
        
        for col in range(target_col + 1, self._width):
            if self._grid[0][col] != col:
                return False

        for col in range(target_col, self._width):
            if self._grid[1][col] != (col + self._width):
                return False

        return True 

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        if self._grid[1][target_col] != 0:
            return False

        for row in range( 2, self._height):
            for col in range( self._width):
                if self._grid[row][col] != (col + row*self._width):
                    return False 

        for col in range( target_col + 1, self._width):
            if self._grid[1][col] != (col + self._width):
                return False

        return True 

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        assert self._grid[0][target_col] == 0, " zero not at (0, target_col) position"
        move_steps = ""
        self.update_puzzle("l")
        self.update_puzzle("d")

        # (0, target_col) is at (0, target_col - 1)
        if self._grid[0][target_col] == target_col:
            move_steps = "ld"
            return move_steps

        curr_row, curr_col = self.current_position( 0, target_col )
        move_steps = self.move_curr_to_target(curr_row, curr_col, 1, target_col - 1)
        move_steps = move_steps + "urdlurrdluldrruld"

        for char in move_steps:
            self.update_puzzle(char)

        return "ld" + move_steps 

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        assert self._grid[1][target_col] == 0, " zero not at (1," + str(target_col) + ") position"
        curr_row, curr_col = self.current_position( 1, target_col)
        move_steps = self.move_curr_to_target( curr_row, curr_col, 1, target_col)
        move_steps = move_steps + "ur" # zero on the left side of (1,target_col)

        self.move_help(move_steps)
        #for char in move_steps:
        #    self.update_puzzle(char)
        return move_steps 

    ###########################################################
    # Phase 3 methods

    def solve_2x2_help(self):
        """ 
        check whether last 2x2 solved
        """
        if self._grid[0][0] == 0 and self._grid[0][1] == 1 \
            and self._grid[1][0] == self._width \
            and self._grid[1][1] == self._width + 1:
            return True
        else:
            return False

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        # check beyond 2x2 is solved
        move_steps = ""
        # move zero to (0,0)
        curr_row, curr_col = self.current_position(0,0)
        if curr_row == 1:
            move_steps += "u"
            self.update_puzzle("u")
        if curr_col == 1:
            move_steps += "l"
            self.update_puzzle("l")

        for _ in range(3):
            if self.solve_2x2_help():
                break
            move_steps += "rdlu"
            self.move_help("rdlu")
        return move_steps 

#    def puzzle_solved(self):
#        """
#        check if solved
#        """
#        for row in range(self._height):
#            for col in range(self._width):
#                if self._grid[row][col] != (col + row*self._width):
#                    return False
#
#        return True

    def move_zero(self, target_row, target_col):
        """
        move zero to target position
        """
        move_steps = ""
        curr_row, curr_col = self.current_position( 0 , 0)
        if target_row > curr_row:
            for _ in range(target_row - curr_row):
                move_steps += "d"
        else:
            for _ in range(curr_row - target_row):
                move_steps += "u"

        if target_col > curr_col:
            for _ in range(target_col - curr_col):
                move_steps += "r"
        else:
            for _ in range(curr_col - target_col):
                move_steps += "l"
        
        # perform move
        self.move_help( move_steps)
        
        return  move_steps 

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        move_steps = ""
        puzzle_solved = True 
        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] != (col + row*self._width):
                    puzzle_solved = False
                    break

        if puzzle_solved:
            return move_steps

        # move zero to lower-right
        move_steps += self.move_zero( self._height -1, self._width - 1) 

        # Phase one
        for row in range(self._height - 1, 1, -1):
            for col in range(self._width - 1, -1, -1):
                if col != 0:
                    move_steps += self.solve_interior_tile(row, col)
                else:       # col == 0
                    move_steps += self.solve_col0_tile(row)

        
        # Phase two
        for col in range(self._width - 1, 1, -1):
            move_steps += self.solve_row1_tile(col)
            move_steps += self.solve_row0_tile(col)

        # Phase three
        move_steps += self.solve_2x2()

        return move_steps 

# Start interactive simulation
#poc_fifteen_gui.FifteenGUI(Puzzle(4, 4))


