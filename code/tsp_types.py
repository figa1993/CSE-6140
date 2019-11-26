import numpy as np

from decimal import Decimal, ROUND_HALF_UP
from collections import deque

class Node:
    __slots__ = 'id', 'x', 'y' # Declare members of class as slots for faster access
    def __init__( self, arglist ):
        self.id = int( arglist[0] )- 1 # Set id member, ZERO INDEXED PER PROJECT REQUIREMENTS
        self.x = float( arglist[1] ) # Set x member
        self.y = float( arglist[2] ) # Set y member

def calculate_edge_cost( src : Node, dest : Node ):
    cost = Decimal(np.sqrt((src.x - dest.x) ** 2 + (src.y - dest.y) ** 2))
    cost = int(cost.quantize(0, rounding=ROUND_HALF_UP))  # Round distance to integer such that 0.5 rounds up


class Edge:
    __slots__ = 'src_id', 'dest_id', 'cost'
    def __init__(self, source_node : Node, dest_node : Node ):
        self.src_id = source_node.id
        self.dest_id = dest_node.id
        # Calculate cost of the edge as euclidian distance
        self.cost = calculate_edge_cost( source_node.id, dest_node.id )

    def __lt__(self, other):
        return self.cost < other.cost

class OutgoingEdge:
    __slots__ = 'dest_id', 'cost'
    def __init__(self, dest_id, cost  ):
        self.dest_id = dest_id
        self.cost = cost

class UndirectedGraph:
    __slots__ = 'node_edges'
    def __init__(self , nodes : [Node]):
        self.node_edges = []*len(nodes) # For each node create a list to store edges
    def add_edge(self, e: Edge  ):
        self.node_edges[e.src_id].append( OutgoingEdge( e.dest_id, e.cost ) )
        self.node_edges[e.dest_id].append(  OutgoingEdge(e.src_id, e.cost ) )


class Solution:
    __slots__ = 'quality', 'node_list'

    # Default constructor
    def __init__(self):
        self.quality = 0
        self.node_list = deque()

    def __init__(self, in_quality, in_node_list ):
        self.quality = in_quality
        self.node_list = in_node_list # Shallow copy

class Trace:
    __slots__ = 'tracepoints'

    def __init__(self):
        self.tracepoints = []

    def add_tracepoint( self, time : float, quality : int ):
        self.tracepoints.append( [ '%.2f'%time, quality ] )

