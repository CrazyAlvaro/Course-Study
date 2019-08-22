"""
Clone of 2048 game.
"""

#import poc_2048_gui        
#import poc_simpletest   # for test
import random

#Directions, DO NOT MODIFY
UP= 1
DOWN= 2
LEFT= 3
RIGHT= 4

#Offsets for computing tile indices in each direction.
#DO NOT MODIFY this dictionary.    
OFFSETS= {UP: (1, 0), 
          DOWN: (-1, 0), 
          LEFT: (0, 1), 
          RIGHT: (0, -1)} 

def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    prev_num, curr_pos = 0, 0
    for pos in range(len(line)):
        if line[pos] != 0:
            if prev_num == 0:
                prev_num = line[pos]
            elif prev_num == line[pos]:
                line[curr_pos] = prev_num * 2
                curr_pos +=1    # set to next pos
                prev_num = 0    # already merged
            else:   
                line[curr_pos] = prev_num
                curr_pos +=1
                prev_num = line[pos]

    if prev_num != 0:
        line[curr_pos] = prev_num
        curr_pos += 1
    
    for pos in range(curr_pos, len(line)):
        line[pos] = 0

    return line

class TwentyFortyEight:
    """
    Class to run the game logic.
    """
    def __init__(self, grid_height, grid_width):
        # replace with your code
        self.row_number = grid_height
        self.col_number = grid_width
        self.grid = [[0 for _ in range(self.col_number)] for _ in range(self.row_number)]     
        #print self.grid
      
        # store the lists of initial tiles
        self.init_tiles = dict()
        self.init_tiles[UP]    = zip([ 0 for i in range(grid_width)], [i for i in range(grid_width)])
        self.init_tiles[DOWN]  = zip([grid_height - 1 for i in range(grid_width)], [i for i in range(grid_width)])
        self.init_tiles[LEFT]  = zip([i for i in range(grid_height)], [0 for i in range(grid_height)])
        self.init_tiles[RIGHT] = zip([i for i in range(grid_height)], [grid_width - 1 for i in range(grid_height)])

        # 9 2s and 1 4
        self.empty_list = list()
        self.new_tile_list = [ 2 for i in range(9)]
        self.new_tile_list.append(4)
        #print self.new_tile_list



    def traverse_empty_tiles(self):
        """ raverse grid and get empty tile position"""
        self.empty_list = list()    # reset list

        for row in range(self.row_number):
            for col in range(self.col_number):
                if self.grid[row][col] == 0:
                    self.empty_list.append( (row,col) )


    def print_init_tiles(self):
        """ 
        print init_tiles, for test purpose
        """
        for key in self.init_tiles.items():
            print (key)

    def reset(self):
        """
        Reset the game so the grid is empty.
        """
        self.grid = [[0 for _ in range(self.col_number)] for _ in range(self.row_number)]     
    
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        grid_str = '' 
        for row in range(self.row_number):
            grid_str += ''.join(str(self.grid[row]))
            grid_str += '\n'
        return grid_str

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self.row_number
    
    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self.col_number 

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        # list_len used to create list
        if direction == UP or direction == DOWN:
            list_len = self.row_number
        else:
            list_len = self.col_number

        tiles = self.init_tiles[direction]
        offset = OFFSETS[direction]
        #print "Offset:" + str(offset) + '\n'

        # get the tile value, call merge function and then set it back
        for tile in tiles:
            #print "current tile:" + str(tile) 
            line = list()

            row, col = tile[0], tile[1] 
            for it_row in range(list_len):
                line.append( self.get_tile(row, col) )
                row, col = row + offset[0], col + offset[1]

            merge(line)

            row, col = tile[0], tile[1] 
            for it_row in range(list_len):
                self.set_tile(row, col, line[it_row])
                row, col = row + offset[0], col + offset[1]
        
        self.new_tile()     # create new tile
    
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty 
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        # question 1: how to randomly select an empty square
            # loop through matrix, record empty tile pos into a list
            # get the list size and generate a random number mod list size, 
            # got the random empty tile pos

        self.traverse_empty_tiles()
        #print self.grid
        #print self.empty_list
        list_size = len(self.empty_list)

        if list_size == 0:      # no new_tile allowed
            return

        rand_pos = random.randint(0, list_size - 1) # 0 <= rand_pos <= list_size -1
        rand_new = random.randint(0,9)

        # question 2: how to generate 2 in 90% and 4 in 10%
            # have a list with 9 2 and 1 4, generate a ramdom index access
        row, col = self.empty_list[rand_pos][0], self.empty_list[rand_pos][1]
        self.set_tile(row, col, self.new_tile_list[rand_new])
    
    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """        
        if row < 0 or row >= self.row_number or col < 0 or col >= self.col_number:
            print "Out of grid bound"
            return -1
        self.grid[row][col] = value
    
    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """        
        if row < 0 or row >= self.row_number or col < 0 or col >= self.col_number:
            print "Out of grid bound"
            return -1
        return self.grid[row][col]

#poc_2048_gui.run_gui(TwentyFortyEight(4, 4))


#def run_test_merge():
#    """ test case for merge functions"""
#    suite = poc_simpletest.TestSuite()
#
#    suite.run_test(merge([2,0, 2, 4]), [4, 4, 0, 0], "Test 1:")
#    suite.run_test(merge([0, 0, 2, 2]), [4, 0, 0, 0], "Test 2:")
#    suite.run_test(merge([2, 2, 0, 0]), [4, 0, 0, 0], "Test 3:")
#    suite.run_test(merge([32, 32, 2, 2]), [64, 4, 0, 0], "Test 4:")
#    suite.run_test(merge([8, 16, 16, 8]), [8, 32, 8, 0], "Test 5:")
#    suite.run_test(merge([2, 2, 2]), [4, 2, 0], "Test 6:")
#    suite.run_test(merge([0, 0, 0]), [0, 0, 0], "Test 7:")
#    suite.run_test(merge([0, 4, 4]), [8, 0, 0], "Test 8:")
#    suite.run_test(merge([32, 16, 16]), [32, 32, 0], "Test 9:")
#    suite.run_test(merge([4, 4]), [8, 0], "Test 10:")
#    suite.run_test(merge([8, 4]), [8, 4], "Test 11:")
#    suite.run_test(merge([2, 2, 4, 8]), [4, 4, 8, 0], "Test 12:")
#    suite.run_test(merge([128, 64, 0, 0]), [128, 64, 0, 0], "Test 13:")
#    suite.run_test(merge([0, 4]), [4, 0], "Test 14:")
#    suite.run_test(merge([32]), [32], "Test 15:")
#    suite.run_test(merge([0]), [0], "Test 16:")
#    suite.run_test(merge([2]), [2], "Test 17:")
#    suite.run_test(merge([4]), [4], "Test 18:")
#    suite.run_test(merge([8]), [8], "Test 19:")
#    suite.run_test(merge([16]), [16], "Test 20:")
#    
#    # Report test result
#    suite.report_results()
#
#def run_test_TwentyFortyEight():
#    """ test case for class TwentyFortyEight """
#    suite = poc_simpletest.TestSuite() 
#
#    inst_4_4 = TwentyFortyEight(4,4)    
#    
#    suite.run_test(inst_4_4.get_grid_height(), 4, "Test get_grid_height")
#    suite.run_test(inst_4_4.get_grid_width(), 4, "Test get_grid_width")
#
#    # set/get_tile Tests
#    inst_4_4.set_tile(2,1,2)
#    suite.run_test(inst_4_4.get_tile(2,1), 2, "Test set/get_tile 1:")
#    inst_4_4.set_tile(3,0,4)
#    suite.run_test(inst_4_4.get_tile(3,0), 4, "Test set/get_tile 2:")
#    inst_4_4.set_tile(1,3,2)
#    suite.run_test(inst_4_4.get_tile(1,3), 2, "Test set/get_tile 3:")
#    inst_4_4.set_tile(0,1,4)
#    suite.run_test(inst_4_4.get_tile(0,1), 4, "Test set/get_tile 4:")
#    inst_4_4.set_tile(1,0,2)
#    suite.run_test(inst_4_4.get_tile(1,0), 2, "Test set/get_tile 5:")
#    
#    #   0 4 0 0
#    #   2 0 0 2
#    #   0 2 0 0
#    #   4 0 0 0 
#    # move tests
#    #print inst_4_4.__str__()
#    inst_4_4.move(UP) 
#    suite.run_test(inst_4_4.get_tile(1,0), 4, "Test move UP")
#    inst_4_4.move(DOWN)
#    suite.run_test(inst_4_4.get_tile(3,0), 4, "Test move DOWN")
#    inst_4_4.move(LEFT)
#    suite.run_test(inst_4_4.get_tile(3,2), 0, "Test move LEFT")
#    inst_4_4.move(RIGHT)
#    suite.run_test(inst_4_4.get_tile(3,1), 0, "Test move RIGHT")
#
#    print "Test new_tile:"
#    print "Before call new_tile:"
#    print inst_4_4.__str__()
#    inst_4_4.new_tile()
#    print "After call new_tile:"
#    print inst_4_4.__str__()
#
#    inst_4_4.reset()
#    suite.run_test(inst_4_4.get_tile(3,3), 0, "Test reset")
#
#    #suite.run_test(
#
#    suite.report_results()
#
#if __name__ == "__main__":
#    print " =============================== "
#    print " ==   Test Merge: phase 1     == "
#    print " =============================== "
#    run_test_merge()
#
#    print "\n\n =============================== "
#    print " ==   Test class: phase 2     == "
#    print " =============================== "
#    run_test_TwentyFortyEight()
#
