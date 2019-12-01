from tsp_types import Solution
from tsp_types import Trace
from tsp_types import Edge
from tsp_types import Node
from tsp_types import UndirectedGraph
from tsp_types import calculate_edge_cost
from tsp_types import Tracepoint
from UnionFind import UnionFindSet, UnionFind, union

from collections import deque
from multiprocessing import Process, Pipe
import time
import bisect

class DfsStackElement:
    __slots__ = 'node_id','outbound_edge_index'
    def __init__(self, node_id : int, outbound_edge_index : int):
        self.node_id = node_id
        self.outbound_edge_index = outbound_edge_index

def mst_approx( union_find : UnionFind, nodes : [Node],edges : [Edge] ):

    n = union_find.n_sets # Cache the number of nodes

    solution = Solution(0)

    ##### Generate MST #####
    mst = UndirectedGraph( nodes )

    # Iterate through undecided edges
    for i in range(len(edges)):
        e = edges[i]
        u = union_find.set_list[e.src_id]
        v = union_find.set_list[e.dest_id]
        # Check if these vertices belong to the same set
        if u.find() != v.find():
            union(u, v)  # Take a union of the sets they belong to
            union_find.n_sets -= 1  # Decrease the number of sets by 1
            mst.add_edge(e)

        if union_find.n_sets == 1:  # MST has been found
            break


    # Depth first search the MST to get a node order
    explore_stack = deque()
    visited_nodes = [False]*n # Create list of flags for which nodes have been visited
    solution.node_list.append( 0 )
    explore_stack.append( DfsStackElement(0,0) )
    visited_nodes[0] = True
    while( len(explore_stack) > 0 ):
        v = explore_stack.pop() # Get the deepest unexplored vertex
        e_list = mst.node_edges[v.node_id]
        for i in range(v.outbound_edge_index,  len(e_list)):
            next = e_list[i].dest_id
            if not visited_nodes[next]: # Check if this outgoing edge goes to an unvisited node
                visited_nodes[next] = True
                solution.node_list.append( next )

                # Add current unexplored node in first and specify to explore next edge in list if possible
                next_outbound_edge_index = i + 1
                if( next_outbound_edge_index < len(e_list) ):
                    explore_stack.append( DfsStackElement( v.node_id, next_outbound_edge_index ) )

                # Add next node to explore next, and specify 0-th edge is to be explored
                explore_stack.append( DfsStackElement( next, 0 ) )

                break # Continue exploration at the newly found node

    ##### Calculate the quality of the solution node sequence #####
    # Begin by calculating distance from first node ( 0 by convention ) and last node in sequence
    solution.quality = calculate_edge_cost( nodes[0], nodes[solution.node_list[-1]] )
    for i in range(1,n):
        # Continue traversing the node sequence and calculating edge cost with the predecessor
        solution.quality += calculate_edge_cost( nodes[solution.node_list[i-1]], nodes[solution.node_list[i]] )

    return solution



def approx( nodes , tracepoint_pipe : Pipe, solution_pipe : Pipe ):

    start_time = time.process_time()  # Get start time in seconds

    n = len(nodes)  # Cache the number of nodes

    # Construct a list of edges sorted by cost
    edge_list = []
    for i in range(n):
        for j in range(i + 1, n):
            # Construct an edge
            e = Edge(nodes[i], nodes[j])
            bisect.insort(edge_list, e)

    m = len(edge_list)  # Cache the number of edges

    union_find = UnionFind()
    for i in range(n):
        set = UnionFindSet(nodes[i])
        union_find.add_set(set)

    solution = mst_approx( union_find, nodes, edge_list )
    solution_pipe.send( solution )
    tracepoint_pipe.send( Tracepoint( time.process_time() - start_time, solution.quality ) )

    exit( 0 ) # Exit the process

def run_approx( nodes , timeout : int ):
    start_time = time.process_time() # Get current uptime in secconds
    solution_read, solution_write = Pipe()
    tracepoint_read, tracepoint_write = Pipe()

    trace = Trace()

    # Create a subprocess which will run the algorithm on another core while this process checks time
    p = Process( target = approx, args = ( nodes, tracepoint_write, solution_write ) )
    p.start() # Start the process

    # Have the thread spin so that it keeps track of time most accurately
    while( ( time.process_time()-start_time ) < timeout and p.is_alive() ):
        if solution_read.poll( 0 ) and tracepoint_read.poll( 0 ):
            # Block until a solution is available or timeout
            solution = solution_read.recv( )

            # Receive corresponding tracepoint and append
            trace.add_tracepoint( tracepoint_read.recv() )

    p.join( 0 ) # Join the subprocess which automatically closes the pipes
    if p.is_alive():
        p.terminate()

    return solution, trace