"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

#import test_suites

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = "obstacle"
HUMAN = "human"
ZOMBIE = "zombie"


class Zombie(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        #self.clear()   this is not correct, calling self
        poc_grid.Grid.clear(self)
        self._zombie_list = []
        self._human_list = []
         
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append( (row,col) )
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)       
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        # replace with an actual generator
        for zombie in self._zombie_list:
            yield zombie 

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append( (row, col) ) 
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list) 
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        # replace with an actual generator
        for human in self._human_list:
            yield human 
        
    def compute_distance_field(self, entity_type):
        """
        Function computes a 2D distance field
        Distance at member of entity_queue is zero
        Shortest paths avoid obstacles and use distance_type distances
        """
        visited = poc_grid.Grid(self.get_grid_height(), self.get_grid_width()) 
        #visited = Grid(self.get_grid_height(), self.get_grid_height()) 
        distance_field = [ [ self.get_grid_height()*self.get_grid_width() \
            for _ in range(self.get_grid_width())] \
            for _ in range(self.get_grid_height())]  
        
        boundary = poc_queue.Queue()
        temp_list = list()
        if entity_type == ZOMBIE:
            temp_list = self._zombie_list
        elif entity_type == HUMAN:
            temp_list = self._human_list
        else:
            print "Unknown entity.\n"
            return distance_field

        for entity in temp_list:
            boundary.enqueue(entity)
            visited.set_full(entity[0], entity[1])
            distance_field[entity[0]][entity[1]] = 0

        while boundary.__len__() > 0:
            current_cell = boundary.dequeue()
            neighbors = self.four_neighbors(current_cell[0], current_cell[1])
            for neighbor in  neighbors:
                if visited.is_empty(neighbor[0], neighbor[1]) \
                    and self.is_empty(neighbor[0], neighbor[1]):

                    visited.set_full(neighbor[0], neighbor[1])
                    boundary.enqueue(neighbor)
                    curr_dist = distance_field[neighbor[0]][neighbor[1]]
                    distance_field[neighbor[0]][neighbor[1]] = min( curr_dist, \
                        distance_field[current_cell[0]][current_cell[1]] + 1)
        return distance_field
            
    
    def move_humans(self, zombie_distance):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        #distance_field = self.compute_distance_field(ZOMBIE)
        new_human_list = list() 
        for human in self._human_list:
            neighbors = self.eight_neighbors(human[0], human[1])
            neighbors.append( (human[0], human[1] ) )
            max_value = -1
            move_cell = (-1,-1)
            for cell in neighbors:
                if zombie_distance[cell[0]][cell[1]] > max_value:
                    max_value = zombie_distance[cell[0]][cell[1]]
                    move_cell = (cell[0], cell[1]) 

            new_human_list.append(move_cell) 
        
        self._human_list = new_human_list
        
    
    def move_zombies(self, human_distance):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        #distance_field = self.compute_distance_field(HUMAN)
        new_zombie_list = list() 
        for zombie in self._zombie_list:
            neighbors = self.four_neighbors(zombie[0], zombie[1])
            neighbors.append( (zombie[0], zombie[1] ) )
            min_value = self.get_grid_height()*self.get_grid_width() 
            move_cell = (-1,-1)
            for cell in neighbors:
                if human_distance[cell[0]][cell[1]] < min_value:
                    min_value = human_distance[cell[0]][cell[1]]
                    move_cell = (cell[0], cell[1]) 

            new_zombie_list.append(move_cell) 
        
        self._zombie_list = new_zombie_list

# Start up gui for simulation - You will need to write some code above
# before this will work without errors

# poc_zombie_gui.run_gui(Zombie(30, 40))
#
#if __name__ == "__main__":
##    print "phase1 test:\n"
#    test_suites.phase1_test(Zombie)
##    print "phase2 test:\n"
#    test_suites.phase2_test(Zombie)
##    print "phase3 test:\n"
#    test_suites.phase3_test(Zombie)
