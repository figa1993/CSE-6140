from tsp_bnb import UnionFindSet
from tsp_bnb import union
from tsp_types import Node
from tsp_types import Edge
import bisect

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