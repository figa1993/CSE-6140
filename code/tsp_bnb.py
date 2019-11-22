from tsp_types import Solution
from tsp_types import Trace
from tsp_types import Edge
from tsp_types import Node

import bisect
import heapq
import numpy as np
import copy

class UnionFindSet:
    __slots__='rank','parent'

    def __init__(self, node : Node ):
        self.rank = 0
        self.parent = self

    def find(self):
        if self.parent != self:
            self.parent = self.parent.find()
        return self.parent

def union( x : UnionFindSet, y : UnionFindSet ):
    x_root = x.find()
    y_root = y.find()
    if x_root.id == y_root.id:
        return

    if x_root.rank == y_root.rank:
        y_root.parent = x_root
        x_root.rank += 1
    elif x_root.rank > y_root.rank:
        y_root.parent = x_root
    else:
        x_root.parent = y_root

class UnionFind:
    __slots__ = 'n_sets', 'set_list'
    def __init__(self):
        self.n_sets = 0
        self.set_list = []
    def add_set(self, set : UnionFindSet):
        self.n_sets += 1
        self.set_list.append( set )

# TODO: turn this into a "PathMaker"
class Graph:
    __slots__ = 'node_degree_list','edge_list', 'degree'
    def __init__(self, n):
        self.node_degree_list = [0]*n
        self.edge_list = []
        self.degree = 0
    def add_edge(self, e):
        self.node_degree_list[ e.src_id] += 1
        self.node_degree_list[ e.dest_id] += 1
        if self.node_degree_list[e.src_id] > self.degree or self.node_degree_list[ e.dest_id] > self.degree:
            self.degree += 1 # since the degree of a node can only increase by 1 when adding any edge
        self.edge_list.append( e )

class Problem:
    __slots__='LB','subgraph','union_find','index'
    def __init__(self, LB : int, subgraph : Graph, union_find : UnionFind, index : int):
        self.LB = LB
        self.subgraph = subgraph
        self.union_find = union_find
        self.index = index
    def __lt__(self, other):
        return self.LB < other.LB

def calculate_lb( edge_list, problem : Problem, parent_lb ):

    # Check if the graph violates path critiera (max degree of any node being 2)
    if problem.subgraph.degree >= 3:
        parent_lb = np.infty

    # Make a deep copy of the union find
    union_find = copy.deepcopy( problem.union_find )
    # union_find = UnionFind()
    # union_find.set_list = current_union_find.set_list[:]
    # union_find.n_sets = current_union_find.n_sets

    # Iterate through undecided edges
    for i in range( problem.index, len(edge_list) ):
        e = edge_list[i]
        u = union_find.set_list[e.src_id]
        v = union_find.set_list[e.dest_id]

        # Check if these vertices belong to the same set
        if u.find() != v.find():
            union(u, v) # Take a union of the sets they belong to
            union_find.n_sets -= 1 # Decrease the number of sets by 1
            parent_lb += e.cost # Add the cost of the edge which joins the sets

    if union_find.n_sets != 1: # There exists no way to create a connected graph with the undecided edges
        parent_lb = np.infty

    # Set the Problem's lower bound
    problem.LB = parent_lb

def calculate_cost( edge_list, problem : Problem ):
    solution = Solution()

    solution.node_list.append( edge_list[0].src_id )
    prev_node = edge_list[1]

    # Because the graph must be a path
    for edge in edge_list :


    # for i in range(0, m):
    #     if solution_id[i]=="1":
    #         solution.quality += edge_list[i].cost
            # solution.node_list =

    # return cost


def bnb( nodes , timeout : int ):

    n = len(nodes) # Cache the number of nodes

    # Construct a list of edges sorted by cost
    edge_list = []
    for i in range(n):
        for j in range(i+1,n):
            # Construct an edge
            e = Edge( nodes[i], nodes[j] )
            bisect.insort( edge_list, e )

    m = len(edge_list) # Cache the number of edges

    union_find = UnionFind()
    for i in range(n):
        set = UnionFindSet( nodes[i] )
        union_find.add_set( set )

    # Construct an empty heapq to represent frontier
    frontier = []

    # Create the root node and added it to frontier
    root = Problem( 0, Graph(), union_find )
    heapq.heappush( frontier,  root)

    best = Solution()

    # Python version of a do-while loop
    while( len(frontier) > 0 ):
        current = heapq.heappop( frontier ) # Pop queue to get most promising node

        e_index = current.index + 1

        # Construct subproblem without the next edge
        child_0 = Problem()
        child_0.index = e_index
        child_0.union_find = copy.deepcopy( current.union_find )
        child_0.LB = calculate_lb( edge_list, child_0, current.LB )

        # Construct subproblem with the next edge
        child_1 = Problem()
        child_1.index = e_index
        child_1.union_find = copy.deepcopy(current.union_find)
        e = edge_list[child_1.index]
        u = child_1.union_find.set_list[e.src_id]
        v = child_1.union_find.set_list[e.dest_id]
        union(u, v)  # Take a union of the sets they belong to
        child_1.subgraph.add_edge( e )
        child_1.LB = calculate_lb( edge_list, child_1, current.LB )

        # Check if these are leaves
        if e_index == m:
            solution = Solution()
            # Check if child_0 is new best

            # update best solution if better than current best

        # else calculate LB and add to frontier if feasible



    trace = Trace()
    trace.add_tracepoint( 0.234, 5 )
    trace.add_tracepoint( 2.4545, 89 )
    return Solution( 0, [ 0, 1, 2 ] ), trace