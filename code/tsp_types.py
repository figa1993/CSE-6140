import numpy as np

class Node:
    __slots__ = 'id', 'x', 'y' # Declare members of class as slots for faster access
    def __init__( self, arglist ):
        self.id = int( arglist[0] )- 1 # Set id member, ZERO INDEXED PER PROJECT REQUIREMENTS
        self.x = float( arglist[1] ) # Set x member
        self.y = float( arglist[2] ) # Set y member

class Edge:
    __slots__ = 'dest', 'cost'
    def __init__(self, source_node : Node, dest_node : Node ):
        self.dest = dest_node
        # Calculate cost of the edge as euclidian distance
        self.cost = np.sqrt( ( source_node.x - dest_node.x)**2 +  ( source_node.y - dest_node.y )**2 )

class Solution:
    __slots__ = 'quality', 'node_list'

    # Default constructor
    def __init__(self):
        self.quality = 0
        self.node_list = []

    def __init__(self, in_quality, in_node_list ):
        self.quality = in_quality
        self.node_list = in_node_list # Shallow copy

class Trace:
    __slots__ = 'tracepoints'

    def __init__(self):
        self.tracepoints = []

    def add_tracepoint( self, time : float, quality : int ):
        self.tracepoints.append( [ '%.2f'%time, quality ] )