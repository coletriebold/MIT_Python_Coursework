# 6.0002 Problem Set 5
# Graph optimization
# Name:
# Collaborators:
# Time:

#
# Finding shortest paths through MIT buildings
import unittest
from graph import Digraph, Node, WeightedEdge

#
# Problem 2: Building up the Campus Map
#
# Problem 2a: Designing your graph
#
# What do the graph's nodes represent in this problem? What
# do the graph's edges represent? Where are the distances
# represented?
#
# Answer:
#


# Problem 2b: Implementing load_map
def load_map(map_filename):
    """
    Parses the map file and constructs a directed graph

    Parameters:
        map_filename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a Digraph representing the map
        class WeightedEdge(Edge):
    def __init__(self, src, dest, total_distance, outdoor_distance):
    """

    graph_obj = Digraph()
    file = map_filename
    with open(file) as fh:
        for i in fh:
            rd = fh.readline()
            rd_list = rd.split(" ")
            if len(rd_list) > 2:
                if '\n' in rd_list[3]:
                    rd_list[3] = rd_list[3][:-1]
                if not graph_obj.has_node(rd_list[0]):
                    graph_obj.add_node(rd_list[0])
                if not graph_obj.has_node(rd_list[1]):
                    graph_obj.add_node(rd_list[1])
                edge_obj = WeightedEdge(rd_list[0], rd_list[1], rd_list[2], rd_list[3])
                graph_obj.add_edge(edge_obj)
    return graph_obj
    print("Loading map from file...")

# Problem 2c: Testing load_map
# Include the lines used to test load_map below, but comment them out


#
# Problem 3: Finding the Shorest Path using Optimized Search Method
#
# Problem 3a: Objective function
#
# What is the objective function for this problem? What are the constraints?
#
# Answer:
#

# Problem 3b: Implement get_best_path
def get_best_path(digraph, start, end, path, max_dist_outdoors, best_dist,
                  best_path):
    """
    Finds the shortest path between buildings subject to constraints.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        path: list composed of [[list of strings], int, int]
            Represents the current path of nodes being traversed. Contains
            a list of node names, total distance traveled, and total
            distance outdoors.
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path
        best_dist: int
            The smallest distance between the original start and end node
            for the initial problem that you are trying to solve
        best_path: list of strings
            The shortest path found so far between the original start
            and end node.

    Returns:
        A tuple with the shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k and the distance of that path.

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then return None.
    """
    best_dist_inside = None
    if len(path) < 1:
        current_paths = []
        node = start
        current_paths.append(node)
        path_dist = 0
    else:
        node = start
        current_paths = path
    
    avail_edges = digraph.get_edges_for_node(node)
    i = 0
    for ea_path in avail_edges:
        destination = ea_path.get_destination()
        if (destination not in current_paths) and (start != end):
            current_paths.append(destination)
            #print(current_paths)
            #path_dist += ea_path.get_outdoor_distance()
            i = 1
            break
        elif start == end:
            i = 2
            break
        elif destination != current_paths[current_paths.index(start)+1]:
            current_paths = current_paths[:(current_paths.index(start)+1)]
            current_paths.append(destination)
            i = 1
            break
    if len(avail_edges) == 0:
        if start == end:
            i = 2
        else:
            i = 0
        
    path_dist = 0
    print(current_paths)
    for k in range(1,len(current_paths)):
        last_edge = digraph.get_edges_for_node(current_paths[k-1])
        for j in last_edge:
            if j.get_destination() == current_paths[k]:
                edge_len = j.get_outdoor_distance()
                break
        path_dist += edge_len
    
    if i == 0:
        print("this triggered1")
        if (current_paths.index(start)-1) >= 0:
            new_start = current_paths[current_paths.index(start)-1]
            #current_paths.pop(len(current_paths)-1)
            [best_dist_inside, current_paths_inside] = get_best_path(digraph, new_start, end, current_paths, max_dist_outdoors, best_dist, best_path)
    
    #Deciding whether or not to continue recursion, and if so, how
    elif i != 2:
        print("this triggered 2")
        if (destination == end) and (path_dist < max_dist_outdoors):
            best_dist = path_dist
            [best_dist_inside, current_paths_inside] = get_best_path(digraph, current_paths[current_paths.index(start)-1], end, current_paths, max_dist_outdoors, best_dist, best_path)
        elif i == 1:
            print("this triggered 3")
            [best_dist_inside, current_paths_inside] = get_best_path(digraph, destination, end, current_paths, max_dist_outdoors, best_dist, best_path)
    else:
        
        return (None, None)
    #comparing values
    if best_dist and best_dist_inside:
        if best_dist < best_dist_inside:
            return (best_dist, current_paths)
        else:
            return (best_dist_inside, current_paths_inside)
    elif best_dist:
        return (best_dist, current_paths)
    else:
        return (best_dist_inside, current_paths_inside)


# Problem 3c: Implement directed_dfs
def directed_dfs(digraph, start, end, max_total_dist, max_dist_outdoors):
    """
    Finds the shortest path from start to end using a directed depth-first
    search. The total distance traveled on the path must not
    exceed max_total_dist, and the distance spent outdoors on this path must
    not exceed max_dist_outdoors.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        max_total_dist: int
            Maximum total distance on a path
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path

    Returns:
        The shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then raises a ValueError.
    """
    # TODO
    pass


# ================================================================
# Begin tests -- you do not need to modify anything below this line
# ================================================================

class Ps2Test(unittest.TestCase):
    LARGE_DIST = 99999

    def setUp(self):
        self.graph = load_map("mit_map.txt")

    def test_load_map_basic(self):
        self.assertTrue(isinstance(self.graph, Digraph))
        self.assertEqual(len(self.graph.nodes), 37)
        all_edges = []
        for _, edges in self.graph.edges.items():
            all_edges += edges  # edges must be dict of node -> list of edges
        all_edges = set(all_edges)
        self.assertEqual(len(all_edges), 129)

    def _print_path_description(self, start, end, total_dist, outdoor_dist):
        constraint = ""
        if outdoor_dist != Ps2Test.LARGE_DIST:
            constraint = "without walking more than {}m outdoors".format(
                outdoor_dist)
        if total_dist != Ps2Test.LARGE_DIST:
            if constraint:
                constraint += ' or {}m total'.format(total_dist)
            else:
                constraint = "without walking more than {}m total".format(
                    total_dist)

        print("------------------------")
        print("Shortest path from Building {} to {} {}".format(
            start, end, constraint))

    def _test_path(self,
                   expectedPath,
                   total_dist=LARGE_DIST,
                   outdoor_dist=LARGE_DIST):
        start, end = expectedPath[0], expectedPath[-1]
        self._print_path_description(start, end, total_dist, outdoor_dist)
        dfsPath = directed_dfs(self.graph, start, end, total_dist, outdoor_dist)
        print("Expected: ", expectedPath)
        print("DFS: ", dfsPath)
        self.assertEqual(expectedPath, dfsPath)

    def _test_impossible_path(self,
                              start,
                              end,
                              total_dist=LARGE_DIST,
                              outdoor_dist=LARGE_DIST):
        self._print_path_description(start, end, total_dist, outdoor_dist)
        with self.assertRaises(ValueError):
            directed_dfs(self.graph, start, end, total_dist, outdoor_dist)

    def test_path_one_step(self):
        self._test_path(expectedPath=['32', '56'])

    def test_path_no_outdoors(self):
        self._test_path(
            expectedPath=['32', '36', '26', '16', '56'], outdoor_dist=0)

    def test_path_multi_step(self):
        self._test_path(expectedPath=['2', '3', '7', '9'])

    def test_path_multi_step_no_outdoors(self):
        self._test_path(
            expectedPath=['2', '4', '10', '13', '9'], outdoor_dist=0)

    def test_path_multi_step2(self):
        self._test_path(expectedPath=['1', '4', '12', '32'])

    def test_path_multi_step_no_outdoors2(self):
        self._test_path(
            expectedPath=['1', '3', '10', '4', '12', '24', '34', '36', '32'],
            outdoor_dist=0)

    def test_impossible_path1(self):
        self._test_impossible_path('8', '50', outdoor_dist=0)

    def test_impossible_path2(self):
        self._test_impossible_path('10', '32', total_dist=100)


if __name__ == "__main__":
    unittest.main()
