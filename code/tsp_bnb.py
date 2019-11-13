from tsp_types import Solution
from tsp_types import Trace
from tsp_types import Edge
from tsp_types import Node

import bisect
import heapq
import numpy as np

class UnionFindSet:
    __slots__='id','rank','parent'

    def __init__(self, node : Node ):
        self.id = node.id
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

class Problem:
    __slots__='LB','id','union_find'
    def __init__(self, in_LB : int, in_id : str, in_union_find : UnionFind):
        self.LB = in_LB
        self.id = in_id
        self.union_find = in_union_find
    def __lt__(self, other):
        return self.LB < other.LB

# def calculate_lb( edge_list, start_index, flags : {}, flag_cost ):
#     flags_copy = flags.copy() # Shallow copy of the flags
#
#     i = start_index
#     while len( flags_copy ) != 0:
#         e = edge_list[i]
#         # If either element can be popped from
#         if flags.has_key( e.src_id,0 ) or flags.has_key( e.dest_id, 0 ):
#             flag_cost += e.cost
#         else:
#             continue

def calculate_lb( edge_list, start_index, current_union_find : UnionFind, current_cost ):

    # Make a shallow copy of the union find
    union_find = UnionFind()
    union_find.set_list = current_union_find.set_list[:]
    union_find.n_sets = current_union_find.n_sets

    # Iterate through undecided edges
    for i in range(start_index, len(edge_list) ):
        e = edge_list[i]
        u = union_find.set_list[e.src_id]
        v = union_find.set_list[e.dest_id]

        # Check if these vertices belong to the same set
        if u.find() != v.find():
            union(u, v) # Take a union of the sets they belong to
            union_find.n_sets -= 1 # Decrease the number of sets by 1
            current_cost += e.cost # Add the cost of the edge which joins the sets

    if union_find.n_sets != 1: # There exists no way to create a connected graph with the undecided edges
        current_cost = np.infty

    return current_cost



def bnb( nodes , timeout : int ):

    n = len(nodes) # Cache the number of nodes

    # Construct a list of edges sorted by cost
    edge_list = []
    for i in range(n):
        for j in range(i+1,n):
            # Construct an edge
            e = Edge( nodes[i], nodes[j] )
            bisect.insort( edge_list, e )


    union_find = UnionFind()
    for i in range(n):
        set = UnionFindSet( nodes[i] )
        union_find.add_set( set )

    # Construct an empty dictionary to memoize node data
    subproblems = {}

    # Construct an empty heapq to represent frontier
    frontier = []

    # Create the root node and added it to frontier
    # flag_dict = {}
    # for node in nodes:
    #     flag_dict[ node.id ] = True
    root = Problem( 0, "", union_find )

    heapq.heappush( frontier,  Problem)

    # Python version of a do-while loop
    while( len(frontier) > 0 ):
        current = heapq.heappop( frontier ) # Pop queue to get most promising node

        # Investigate both expansions


        # Check if these are leaves
            # update best solution if better than current best
        # else calculate LB and add to frontier if feasible



    trace = Trace()
    trace.add_tracepoint( 0.234, 5 )
    trace.add_tracepoint( 2.4545, 89 )
    return Solution( 0, [ 0, 1, 2 ] ), trace