#######################################################################################################################
# File: UnionFind.py
# Description : File containing the definition of the union find class used in all Minimum Spanning Tree calculations
#######################################################################################################################
from tsp_types import Node
from tsp_types import Edge
import bisect

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
    if x_root == y_root:
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

if __name__ == '__main__':
    nodes = []
    nodes.append( Node( [1, 0, 0 ] ) )
    nodes.append( Node( [2, 0, 1 ] ) )
    nodes.append( Node( [3, 1, 0 ] ) )

    n = len(nodes) # Cache the number of nodes

    # Construct a list of edges sorted by cost
    edge_list = []
    for i in range(n):
        for j in range(i+1,n):
            # Construct an edge
            e = Edge( nodes[i], nodes[j] )
            bisect.insort( edge_list, e )

    union_find = []
    for i in range(n):
        union_find.append( UnionFindSet( nodes[i] ) )

    for e in edge_list:
        u = union_find[e.src_id]
        v = union_find[e.dest_id]
        if u.find() != v.find():
            union( u, v )