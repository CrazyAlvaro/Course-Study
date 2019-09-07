# Fall 2012 6.034 Lab 2: Search
#
# Your answers for the true and false questions will be in the following form.
# Your answers will look like one of the two below:
#ANSWER1 = True
#ANSWER1 = False

# 1: True or false - Hill Climbing search is guaranteed to find a solution
#    if there is a solution
ANSWER1 = False

# one: local maximum is infinite
# two: no goal node known, local maximum
# three: not allow backtracking


# 2: True or false - Best-first search will give an optimal search result
#    (shortest path length).
#    (If you don't know what we mean by best-first search, refer to
#     http://courses.csail.mit.edu/6.034f/ai3/ch4.pdf (page 13 of the pdf).)
ANSWER2 = False

# 3: True or false - Best-first search and hill climbing make use of
#    heuristic values of nodes.
ANSWER3 = True

# 4: True or false - A* uses an extended-nodes set.
ANSWER4 = True

# 5: True or false - Breadth first search is guaranteed to return a path
#    with the shortest number of nodes.
ANSWER5 = True

# 6: True or false - The regular branch and bound uses heuristic values
#    to speed up the search for an optimal path.
ANSWER6 = False

# Import the Graph data structure from 'search.py'
# Refer to search.py for documentation
from search import Graph

## Optional Warm-up: BFS and DFS
# If you implement these, the offline tester will test them.
# If you don't, it won't.
# The online tester will not test them.

def bfs(graph, start, goal):
    # based on book's algorithm
    def bfs_search(graph, start, goal):
        paths = [[start]]
        extended_nodes = set([start])

        while len(paths) > 0:
            curr_path = paths.pop(0)
            if curr_path[-1] == goal:
                return curr_path

            adjacents = graph.get_connected_nodes(curr_path[-1])
            for adj in adjacents:
                if not adj in extended_nodes:
                    extended_nodes.add(adj)
                    new_path = curr_path[:]
                    new_path.append(adj)
                    paths.append(new_path)

        # no more paths
        return []


    def bfs_visit(node_paths):
        next_paths = []
        if len(node_paths) == 0:
            return []

        # extends current paths
        for path in node_paths:
            curr = path[-1]
            if curr == goal:
                return path

            adjacents = graph.get_connected_nodes(curr)
            for adj in adjacents:
                if not adj in extended_nodes:
                    extended_nodes.add(adj)
                    new_path = path[:]
                    new_path.append(adj)
                    next_paths.append(new_path)

        return bfs_visit(next_paths)

    # extended_nodes = set()
    # return bfs_visit([[start]])
    return bfs_search(graph, start, goal)



## Once you have completed the breadth-first search,
## this part should be very simple to complete.
def dfs(graph, start, goal):
    def is_visited(node):
        if node in extended_nodes:
            return True
        else:
            return False

    def dfs_visit(curr, path):
        # return path if start == goal
        if found_obj['found'] or is_visited(curr):
            return

        extended_nodes.add(curr)
        if len(path) == 0:
            path.append(curr)

        if curr == goal:
            found_obj['found'] = True
            return path

        # get adjacent nodes,
        connected_nodes = graph.get_connected_nodes(curr)

        # visit all adjacent nodes
        for node in connected_nodes:
            path.append(node)
            dfs_visit(node, path)
            if found_obj['found']:
                return path
            else:
                path.pop()

        return []


    # extended_nodes = set()
    # found_obj = {'found': False}
    # return dfs_visit(start, [])

    # Another implementation based on book
    def dfs_search(graph, start, goal):
        paths = [[start]]
        extended_nodes = set([start])

        while len(paths) > 0:
            curr_path = paths.pop(0)
            if curr_path[-1] == goal:
                return curr_path

            adjacents = graph.get_connected_nodes(curr_path[-1])
            for adj in adjacents:
                if not adj in extended_nodes:
                    extended_nodes.add(adj)
                    new_path = curr_path[:]
                    new_path.append(adj)
                    paths.insert(0, new_path)

        # no more paths
        return []

    return dfs_search(graph, start, goal)



## Now we're going to add some heuristics into the search.
## Remember that hill-climbing is a modified version of depth-first search.
## Search direction should be towards lower heuristic values to the goal.
def hill_climbing(graph, start, goal):
    """ hill_climbing doesn't need extended_nodes checking but need to check loop """
    paths = [[start]]

    while len(paths) > 0:
        curr_path = paths.pop(0)
        if curr_path[-1] == goal:
            return curr_path

        new_paths = []
        adjacents = graph.get_connected_nodes(curr_path[-1])
        """ filter adjacent already within curr_path """
        adjacents = filter(lambda adj: curr_path.count(adj) == 0, adjacents)

        for adj in adjacents:
            new_path = curr_path[:]
            new_path.append(adj)
            new_paths.append(new_path)

        """ hill_climbing diff from Depth First Search, Sort by the estimate distance """
        new_paths.sort(key=lambda path: graph.get_heuristic(path[-1], goal))

        """ add new_paths at front """
        paths = new_paths + paths

    # no more paths
    return []

## Now we're going to implement beam search, a variation on BFS
## that caps the amount of memory used to store paths.  Remember,
## we maintain only k candidate paths of length n in our agenda at any time.
## The k top candidates are to be determined using the
## graph get_heuristic function, with lower values being better values.
def beam_search(graph, start, goal, beam_width):
    def beam_visit_level(paths):
        next_paths = []

        """ Not found """
        if len(paths) == 0: return []

        for path in paths:
            curr = path[-1]
            if curr == goal: return path

            adjacents = graph.get_connected_nodes(curr)

            """ filter adjacent already within path to avoid loop """
            adjacents = filter(lambda adj: path.count(adj) == 0, adjacents)

            for adj in adjacents:
                new_path = path[:]
                new_path.append(adj)
                next_paths.append(new_path)

        """ select the first beam_width paths sorted by heuristic value """
        next_paths.sort(key=lambda path: graph.get_heuristic(path[-1], goal))
        return beam_visit_level(next_paths[:beam_width])

    return beam_visit_level([[start]])

## Now we're going to try optimal search.  The previous searches haven't
## used edge distances in the calculation.

## This function takes in a graph and a list of node names, and returns
## the sum of edge lengths along the path -- the total distance in the path.
def path_length(graph, node_names):
    """ Assume the path is valid """
    if len(node_names) <= 1:
        return 0
    else:
        edge = graph.get_edge(node_names[0], node_names[1])
        return edge.length + path_length(graph, node_names[1:])


def branch_and_bound(graph, start, goal):
    paths = [[start]]

    while len(paths) > 0:
        curr_path = paths.pop(0)
        if curr_path[-1] == goal:
            return curr_path

        new_paths = []
        adjacents = graph.get_connected_nodes(curr_path[-1])
        """ filter loop """
        adjacents = filter(lambda adj: curr_path.count(adj) == 0, adjacents)

        for adj in adjacents:
            new_path = curr_path[:]
            new_path.append(adj)
            new_paths.append(new_path)

        paths += new_paths
        paths.sort(key=lambda path: path_length(graph, path))

    # no more paths
    return []

def a_star(graph, start, goal):
    paths = [[start]]

    """ Note: use extended-list makes A-Star search admissible but not consistent """
    extended_nodes = set([start])

    while len(paths) > 0:
        curr_path = paths.pop(0)
        if curr_path[-1] == goal:
            return curr_path

        new_paths = []
        adjacents = graph.get_connected_nodes(curr_path[-1])
        """ filter loop """
        adjacents = filter(lambda adj: curr_path.count(adj) == 0, adjacents)

        for adj in adjacents:
            if not adj in extended_nodes:
                extended_nodes.add(adj)
                new_path = curr_path[:]
                new_path.append(adj)
                new_paths.append(new_path)

        paths += new_paths

        """ remove redundant paths end same node, keep the one with least length """
        paths.sort(key=lambda path: path_length(graph, path))
        visited_nodes = set()
        for path in paths:
            if not path[-1] in visited_nodes:
                visited_nodes.add(path[-1])
            else:
                paths.remove(path)

        """ sort based on current length and heuristic length """
        paths.sort(key=lambda path: path_length(graph, path) + graph.get_heuristic(path[-1], goal))

    # no more paths
    return []


## It's useful to determine if a graph has a consistent and admissible
## heuristic.  You've seen graphs with heuristics that are
## admissible, but not consistent.  Have you seen any graphs that are
## consistent, but not admissible?

def shortest_path(graph, start, goal):
    return branch_and_bound(graph, start, goal)

def is_admissible(graph, goal):
    """
    admissible: the heuristic value for every node in a graph must be less than
                or equal to the distance of the shortest path from the goal to that node
    """
    checked_nodes = set()
    nodes = [goal]

    while len(nodes) > 0:
        curr = nodes.pop(0)

        if not curr in checked_nodes:
            checked_nodes.add(curr)
            nodes.extend(graph.get_connected_nodes(curr))
        else:
            continue

        """ check if heuristic value <= shortest length """
        if not graph.get_heuristic(curr, goal) <= path_length(graph, shortest_path(graph, curr, goal)):
            return False

    # End of while
    return True

def is_consistent(graph, goal):
    """
    consistent: for each edge in the graph, the edge length must be greater than
                or equal to the absolute value of the difference
                between the two heuristic values of its nodes.
    """
    checked_nodes = set()
    checked_edges = set()
    nodes = [goal]


    while len(nodes) > 0:
        curr = nodes.pop(0)

        if not curr in checked_nodes:
            checked_nodes.add(curr)
            adjs = graph.get_connected_nodes(curr)
            nodes.extend(adjs)

            for adj in adjs:
                """ check edge >= absolute value of the two nodes' heuristic difference """
                curr_edge = graph.get_edge(curr, adj)
                if curr_edge in checked_edges:
                    continue
                elif not curr_edge.length >= abs(graph.get_heuristic(curr, goal) - graph.get_heuristic(adj, goal)):
                    return False
                else:
                    checked_edges.add(curr_edge)

    # End of While
    return True


HOW_MANY_HOURS_THIS_PSET_TOOK = '10'
WHAT_I_FOUND_INTERESTING = """
bfs: use a queue
dfs: use a stack
hill_climbing: similiar to bfs, only sort by heuristic value
beam: limit the extends nodes based on heuristic value
branch_and_bound: extends shortest path in queue until found the path
A*: use current path length + heuristic estimate, remove redundant nodes path
"""
WHAT_I_FOUND_BORING = 'Nothing'
