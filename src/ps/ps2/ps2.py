# 6.0002 Problem Set 5

#
# Finding shortest paths through MIT buildings
#
import unittest
from graph import Digraph, Node, WeightedEdge
from copy import deepcopy

#
# Problem 2: Building up the Campus Map
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
    """
    # read map-file
    mapFile = open(map_filename, "r")
    mitGraph = Digraph()
    nodeMap = dict()
    # each entry
    for line in mapFile:
        # [src, dest, total dist, outdoot dist]
        info = line.strip("\n").split(" ")
        for i in range(2):
            if not info[i] in nodeMap:
                thisNode = Node(info[i])
                mitGraph.add_node(thisNode)
                nodeMap[info[i]] = thisNode
        mitGraph.add_edge(
            WeightedEdge(nodeMap[info[0]], nodeMap[info[1]], int(info[2]), int(info[3]))
        )
    return mitGraph


#
# Problem 3: Finding the Shorest Path using Optimized Search Method
#

# Problem 3b: Implement get_best_path
def get_best_path(digraph, start, end, path, max_dist_outdoors, best_dist, best_path):
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
    # instantiate Nodes
    startNode = Node(start)
    endNode = Node(end)
    # ensure valid Nodes
    if not (digraph.has_node(startNode) and digraph.has_node(endNode)):
        raise
    # ensure within constraints
    elif not (path[1] <= best_dist and path[2] <= max_dist_outdoors):
        return None
    # insert start into currPath
    path = deepcopy(path)
    path[0].append(start)
    # check if path can be estabilished
    if start == end:
        # update the best path
        best_path = path[0]
    # proceed to search for a path through the edges
    else:
        for edge in digraph.get_edges_for_node(startNode):
            dest = edge.get_destination()
            destName = dest.get_name()
            # avoid cycles
            if destName in path[0]:
                continue
            # update path
            path[1] += edge.get_total_distance()
            path[2] += edge.get_outdoor_distance()
            # possible path
            possPath = get_best_path(
                digraph, destName, end, path, max_dist_outdoors, best_dist, best_path
            )
            if possPath is not None:
                pathDist = 0
                for i in range(0, len(possPath) - 1, 1):
                    for jEdge in digraph.get_edges_for_node(Node(possPath[i])):
                        if jEdge.get_destination().get_name() == possPath[i + 1]:
                            pathDist += jEdge.get_total_distance()
                            break
                best_dist = pathDist
                best_path = possPath
            # reset path
            path[1] -= edge.get_total_distance()
            path[2] -= edge.get_outdoor_distance()
    # returning results
    if not best_path:
        return None
    return best_path


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
    path = [[], 0, 0]
    bestPath = get_best_path(
        digraph, start, end, path, max_dist_outdoors, max_total_dist, []
    )
    if bestPath is None:
        raise ValueError
    return bestPath


# ================================================================
# Begin tests -- you do not need to modify anything below this line
# ================================================================


class Ps2Test(unittest.TestCase):
    LARGE_DIST = 99999

    def setUp(self):
        self.graph = load_map("src/ps/ps2/mit_map.txt")

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
            constraint = "without walking more than {}m outdoors".format(outdoor_dist)
        if total_dist != Ps2Test.LARGE_DIST:
            if constraint:
                constraint += " or {}m total".format(total_dist)
            else:
                constraint = "without walking more than {}m total".format(total_dist)

        print("------------------------")
        print("Shortest path from Building {} to {} {}".format(start, end, constraint))

    def _test_path(self, expectedPath, total_dist=LARGE_DIST, outdoor_dist=LARGE_DIST):
        start, end = expectedPath[0], expectedPath[-1]
        self._print_path_description(start, end, total_dist, outdoor_dist)
        dfsPath = directed_dfs(self.graph, start, end, total_dist, outdoor_dist)
        print("Expected: ", expectedPath)
        print("DFS: ", dfsPath)
        self.assertEqual(expectedPath, dfsPath)

    def _test_impossible_path(
        self, start, end, total_dist=LARGE_DIST, outdoor_dist=LARGE_DIST
    ):
        self._print_path_description(start, end, total_dist, outdoor_dist)
        with self.assertRaises(ValueError):
            directed_dfs(self.graph, start, end, total_dist, outdoor_dist)

    def test_path_one_step(self):
        self._test_path(expectedPath=["32", "56"])

    def test_path_no_outdoors(self):
        self._test_path(expectedPath=["32", "36", "26", "16", "56"], outdoor_dist=0)

    def test_path_multi_step(self):
        self._test_path(expectedPath=["2", "3", "7", "9"])

    def test_path_multi_step_no_outdoors(self):
        self._test_path(expectedPath=["2", "4", "10", "13", "9"], outdoor_dist=0)

    def test_path_multi_step2(self):
        self._test_path(expectedPath=["1", "4", "12", "32"])

    def test_path_multi_step_no_outdoors2(self):
        self._test_path(
            expectedPath=["1", "3", "10", "4", "12", "24", "34", "36", "32"],
            outdoor_dist=0,
        )

    def test_impossible_path1(self):
        self._test_impossible_path("8", "50", outdoor_dist=0)

    def test_impossible_path2(self):
        self._test_impossible_path("10", "32", total_dist=100)


if __name__ == "__main__":
    unittest.main()
