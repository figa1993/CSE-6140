from tsp_types import Solution
from tsp_types import Trace
from tsp_types import Edge
from tsp_types import Node
from tsp_types import UndirectedGraph
from tsp_types import calculate_edge_cost
from tsp_types import Tracepoint
from tsp_types import Trace
from UnionFind import UnionFindSet, UnionFind, union
from tsp_approx import mst_approx

from multiprocessing import Process, Pipe
import bisect
import heapq
import numpy as np
import copy
import time

class Problem:
    __slots__='LB','subgraph','subgraph_cost','union_find','index'
    def __init__(self, LB : int = 0 , subgraph : UndirectedGraph = None , subgraph_cost : int = 0,
                 union_find : UnionFind = None, index  : int = -1):
        self.LB = LB
        self.subgraph = subgraph
        self.union_find = union_find
        self.index = index
        self.subgraph_cost = subgraph_cost
    def __lt__(self, other):
        return self.LB < other.LB

def calculate_lb( edge_list, problem : Problem ):

    problem.LB = problem.subgraph_cost

    # Make a deep copy of the union find
    union_find = copy.deepcopy( problem.union_find )

    # Iterate through undecided edges
    for i in range( problem.index, len(edge_list) ):
        e = edge_list[i]
        u = union_find.set_list[e.src_id]
        v = union_find.set_list[e.dest_id]

        # Check if these vertices belong to the same set
        if u.find() != v.find():
            union(u, v) # Take a union of the sets they belong to
            union_find.n_sets -= 1 # Decrease the number of sets by 1
            problem.LB += e.cost # Add the cost of the edge which joins the sets
        if union_find.n_sets == 1: # MST has been found
            break

    if union_find.n_sets != 1: # There exists no way to create a connected graph with the undecided edges
        problem.LB = np.infty

def generate_solution( edge_list : [ Edge ], node_list : [ Node ], problem : Problem  ):
    solution = Solution()

    # Traverse the graph to generate path and its cost
    # Traverse along the first edge
    prev = 0
    next = problem.subgraph.node_edges[0][0].dest_id
    # Add the nodes to the deque
    solution.node_list.append(next)
    solution.node_list.append(0)
    solution.quality = problem.subgraph.node_edges[0][0].cost
    while len(problem.subgraph.node_edges[next]) == 2 :
        if problem.subgraph.node_edges[next][0].dest_id == prev:
            # The first edge in the next node returns to previous, traverse along second edge
            e = problem.subgraph.node_edges[next][1]
        else:
            # The 2nd edge in the next node returns to previous, traverse along first edge
            e = problem.subgraph.node_edges[next][0]
        prev = next
        next = e.dest_id
        solution.node_list.appendleft(next) # Add the next node to the LEFT SIDE of deque
        solution.quality += e.cost # Add the edge cost to the solution quality

    # Traverse along the second edge (if applicable)
    prev = 0
    if( len(problem.subgraph.node_edges[prev]) == 2 ):
        next = problem.subgraph.node_edges[0][1].dest_id
        solution.node_list.append(next)
        solution.quality += problem.subgraph.node_edges[0][1].cost
        while len(problem.subgraph.node_edges[next]) == 2:
            if problem.subgraph.node_edges[next][0].dest_id == prev:
                # The first edge in the next node returns to previous, traverse along second edge
                e = problem.subgraph.node_edges[next][1]
            else:
                # The 2nd edge in the next node returns to previous, traverse along first edge
                e = problem.subgraph.node_edges[next][0]
            prev = next
            next = e.dest_id
            solution.node_list.append(next) # Add the next node to the RIGHT SIDE of deque
            solution.quality += e.cost # Add the edge cost to the solution quality

    # Add the final edge between last node and first node
    solution.quality +=  calculate_edge_cost( node_list[solution.node_list[0]], node_list[solution.node_list[-1]] )

    return solution

def bnb( nodes,  tracepoint_pipe : Pipe, solution_pipe : Pipe ):

    start_time = time.process_time() # Get start time in seconds

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
    root = Problem( int(0), UndirectedGraph( nodes ), 0, union_find, 0 )
    heapq.heappush( frontier,  root)

    # Initialize the solution with a 2MST approximation, so that branches get pruned sooner
    best = mst_approx( copy.deepcopy(union_find), nodes, edge_list )
    print("best quality {}".format(best.quality))
    print("best sequence:\t{}".format(best.node_list))

    iter = 0
    while( len(frontier) > 0 ):
        iter +=1
        print(iter)
        current = heapq.heappop( frontier ) # Pop queue to get most promising node

        e_index = current.index + 1

        # Construct subproblem without the next edge
        child_0 = Problem()
        child_0.subgraph = copy.deepcopy( current.subgraph )
        child_0.subgraph_cost = current.subgraph_cost
        child_0.index = e_index
        child_0.union_find = copy.deepcopy( current.union_find )
        calculate_lb( edge_list, child_0 )

        # Check if the answers to subproblem can be better than best answer so far
        if(  child_0.LB < best.quality ):
            # Add the subproblem to the frontier
            heapq.heappush( frontier, child_0 )
            print("adding child 0 subproblem with lower bound= {}".format(child_0.LB))
        else:
            print("pruning non-promising child 0 subproblem")

        # Construct subproblem with the next edge
        e = edge_list[current.index] # Get the edge to add
        # Check if path condition ( degree of every node < 3 ) will not be violated
        if len(current.subgraph.node_edges[e.src_id]) < 2 and len(current.subgraph.node_edges[e.dest_id]) < 2:
            child_1 = Problem()
            child_1.subgraph = copy.deepcopy(current.subgraph)
            child_1.subgraph_cost = current.subgraph_cost
            child_1.union_find = copy.deepcopy(current.union_find)
            u = child_1.union_find.set_list[e.src_id]
            v = child_1.union_find.set_list[e.dest_id]
            # Check if these vertices belong to the same set
            if u.find() != v.find():
                union(u, v)  # Take a union of the sets they belong to
            else: # This edge will create an internal cycle, thus it creates infeasible subproblems
                print("pruning subproblems with cycle")
                continue
            child_1.union_find.n_sets -= 1 # Decrement the number of sets

            child_1.subgraph.add_edge(e)
            child_1.subgraph_cost += e.cost
            if( child_1.union_find.n_sets == 1 ):
                # This is a fully connected graph with each node degree <=2 i.e. a simple path which is a sol'n
                new_solution = generate_solution( edge_list, nodes, child_1 )
                if new_solution.quality < best.quality: # Check if this is the new best solution
                    best = new_solution # Update best solution found so far
                    # Write to the tracefile
                    # tracefile_handle.write("{:.2f},{}".format( [time.process_time()-start_time, best.quality] ) )
                    tracepoint_pipe.send( Tracepoint( time.process_time() - start_time, best.quality ) )
                    solution_pipe.send( best )
                    print( "best quality %d".format(best.quality) )
                    print("best sequence:\t{}".format(best.node_list))
            else:
                # This is a new subproblem
                child_1.index = e_index
                calculate_lb( edge_list, child_1 )
                # Check if the answers to subproblem can be better than best answer so far
                if( child_1.LB < best.quality):
                    # Add the subproblem to the frontier
                    heapq.heappush(frontier, child_1)
                    print("adding child 1 subproblem with lower bound= {}".format(child_1.LB))
                else:
                    print( "pruning non-promising child 1 subproblem" )
    exit( 0 )


def run_bnb(nodes , timeout : int ):
    start_time = time.process_time() # Get current uptime in secconds
    solution_read, solution_write = Pipe()
    tracepoint_read, tracepoint_write = Pipe()

    trace = Trace()

    # Create a subprocess which will run the algorithm on another core while this process checks time
    p = Process( target = bnb, args = (nodes, tracepoint_write, solution_write ) )
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