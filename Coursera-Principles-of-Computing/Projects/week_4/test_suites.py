#Testing suite for Zombies BFS class

import poc_simpletest as test
import random

OBSTACLE = "obstacle"
HUMAN = "human"
ZOMBIE = "zombie"

def phase1_test(Zombie):
    print "Phase 1 tests"
    phase1 = test.TestSuite()
    height = 10
    width = 20
    blank_grid = Zombie(height, width)
    filled_grid = Zombie(height, width, [(0, 4), (1, 3), (2, 2), (3, 1), (4, 0)], [(1, 1), (4, 2)], [(1, 2), (2, 3), (3, 4)])
    
    #testing num_zombies
    phase1.run_test(filled_grid.num_zombies(), 2, "Failed num_zombies method")
    
    #testing num_humans
    phase1.run_test(filled_grid.num_humans(), 3, "Failed num_humans method")
    
    #testing add_zombie
    zombie_count = 5
    zombie_list = []
    for dummy_count in range(zombie_count):
        zombie_list.append((random.randrange(height), random.randrange(width)))
    for zomb in zombie_list:
        blank_grid.add_zombie(zomb[0], zomb[1])
    phase1.run_test(blank_grid.num_zombies(), zombie_count, "Failed add_zombies method")
    
    #testing add_human
    human_count = 7
    human_list = []
    for dummy_count in range(human_count):
        human_list.append((random.randrange(height), random.randrange(width)))
    for hum in human_list:
        blank_grid.add_human(hum[0], hum[1])
    phase1.run_test(blank_grid.num_humans(), human_count, "Failed add_humans method")
    
    #testing zombies
    zombie_counter = 0
    for zomb in blank_grid.zombies():
        phase1.run_test(zomb, zombie_list[zombie_counter], "Failed zombies method")
        zombie_counter += 1
        
    #testing humans
    human_counter = 0
    for hum in blank_grid.humans():
        phase1.run_test(hum, human_list[human_counter], "Failed humans method")
        human_counter += 1
    
    #testing clear
    blank_grid.clear()
    phase1.run_test(blank_grid.num_zombies(), 0, "Failed clear method. Zombies not cleared")
    phase1.run_test(blank_grid.num_humans(), 0, "Failed clear method. Humans not cleared")
    has_obstacle = False
    for row in range(height):
        for col in range(width):
            if not blank_grid.is_empty(row, col):
                has_obstacle = True
    phase1.run_test(has_obstacle, False, "Failed clear method. Obstacles not cleared")
    
    phase1.report_results()

def phase2_test(Zombie):
    print "Phase 2 tests"
    height = 20
    width = 30
    obstacle_list = [(4, 15), (5, 15), (6, 15), (7, 15), (8, 15), (9, 15), (10, 15), (11, 15), (12, 15), (13, 15), (14, 15), (15, 10), (15, 11), (15, 12), (15, 13), (15, 14), (15, 15)]
    entity_list = [(7, 12), (12, 12)]
    expected_distance = [[19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24], [18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23], [17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22], [16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21], [15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 4, 5, 600, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22], [14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 3, 4, 600, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23], [13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 2, 3, 600, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24], [12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, 1, 2, 600, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25], [13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 2, 3, 600, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26], [14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 3, 4, 600, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27], [14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 3, 4, 600, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28], [13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 2, 3, 600, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29], [12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, 1, 2, 600, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30], [13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 2, 3, 600, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30], [14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 3, 4, 600, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29], [15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 600, 600, 600, 600, 600, 600, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28], [16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27], [17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28], [18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29], [19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]]
    phase2 = test.TestSuite()
    obstacles_zombies = Zombie(height, width, obstacle_list, entity_list)
    obstacles_humans = Zombie(height, width, obstacle_list, [], entity_list)
    phase2.run_test(obstacles_zombies.compute_distance_field(ZOMBIE),
                    expected_distance, "Failed distance test with zombie")
    phase2.run_test(obstacles_humans.compute_distance_field(HUMAN),
                    expected_distance, "Failed distance test with human")

    height = 3
    width = 3
    entity_list = [(1, 1)]
    expected_distance = [[2, 1, 2], [1, 0, 1], [2, 1, 2]]
    zombie_on_human = Zombie(height, width, [], entity_list, entity_list)
    phase2.run_test(zombie_on_human.compute_distance_field(ZOMBIE),
                    expected_distance, "Failed zombie distance test with a zombie eating a human")
    phase2.report_results()

def phase3_test(Zombie):
    phase3 = test.TestSuite()
    print "Phase 3 tests"
    
    #testing humans
    obj1 = Zombie(3, 3, [], [(2, 2)], [(1, 1)])
    dist1 = [[4, 3, 2], [3, 2, 1], [2, 1, 0]]
    exp1 = [(0, 0)]
    obj1.move_humans(dist1)
    human_list = []
    for hum in obj1.humans():
        human_list.append(hum)
    phase3.run_test(human_list, exp1, "Failed human move test")
    
    #testing zombies
    obj2 = Zombie(3, 3, [], [(1, 1)], [(1, 1)])
    dist2 = [[2, 1, 2], [1, 0, 1], [2, 1, 2]]
    exp2 = [(1, 1)]
    obj2.move_zombies(dist2)
    zombie_list = []
    for zomb in obj2.zombies():
        zombie_list.append(zomb)
    phase3.run_test(zombie_list, exp2, "Failed zombie move test")
    
    #testing zombie eating a human
    height = 3
    width = 3
    entity_list = [(1, 1)]
    distance_list = [[2, 1, 2], [1, 0, 1], [2, 1, 2]]
    zombie_on_human = Zombie(height, width, [], entity_list, entity_list)
    zombie_list = []
    for zomb in zombie_on_human.zombies():
        zombie_list.append(zomb)
    phase3.run_test(zombie_list, entity_list, "Failed zombie move test when zombie eating a human")
    
    phase3.report_results()