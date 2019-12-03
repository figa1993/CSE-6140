from tsp_types import Solution
from tsp_types import Trace
from tsp_types import Node
from tsp_types import Edge
from tsp_types import Tracepoint
import random
import numpy as np
import math
import time
import copy

from multiprocessing import Process, Pipe


def distance_calculator(nodes):
    num_locs = len(nodes)
    mat = np.empty((num_locs,num_locs), dtype=Edge)
    for x in range(num_locs):
        for y in range(num_locs):
            mat[x,y] = Edge(nodes[x],nodes[y])
            if x == y:
                mat[x,y].cost = np.inf
    return mat

def get_min_cost(dest_group,rem_nodes):
    min_cost = np.inf
    min_index = np.inf
    for i in range (0,dest_group.shape[0]):
        if (dest_group[i].cost < min_cost) and rem_nodes[i] == 1:
            min_cost = dest_group[i].cost
            min_index = i
    return min_cost, min_index

#This will solve a greedy problem to give us a place to start
def greedy_heuristic(dist_matrix,index_start):
    initialdist_matrix = dist_matrix
    start_index = index_start #random.randint(0,dist_matrix.shape[0]-1)
    total_cost = 0
    route = []
    rem_nodes = np.ones(dist_matrix.shape[0])
    rem_nodes[start_index] = 0
    route.append(start_index)
    while rem_nodes.any(): #while there are still unused locations
        dist,next_hop = get_min_cost(dist_matrix[start_index,],rem_nodes)
        route.append(next_hop)
        start_index = next_hop
        rem_nodes[next_hop] = 0
        total_cost += dist
    total_cost += initialdist_matrix[route[len(route)-1],route[0]].cost
    route.append(route[0])
    return route,total_cost

def calculate_route_cost(route,cost_matrix):
    cost = 0
    for i in range(0,len(route)-1):
        cost += cost_matrix[route[i],route[i+1]].cost
    return cost


def two_opt(dist_matrix,nodes,start_nodes,tracepoint_pipe : Pipe, solution_pipe : Pipe):
    start_time = time.process_time()
    initial = 1
    mat = distance_calculator(nodes)

    for x in start_nodes:
        greedy_route,greedy_total_cost = greedy_heuristic(mat,x)
        route_matrix = greedy_route # Use greedy heuristic solution as the starting point
        if initial == 1:
            bestroute = greedy_route
            bestcost = greedy_total_cost
            initial = 0
        for i in range(1,len(route_matrix)-1):
            for k in range(i+i,len(route_matrix)):
                improved_route = route_matrix[:]
                improved_route[i:k] = route_matrix[k-1:i-1:-1] #Here we will take the section to flip and flip it and replace the order.
                new_cost = calculate_route_cost(improved_route,dist_matrix)
                if new_cost < bestcost:
                    # print("Improvement by 2opt made")
                    bestroute = improved_route
                    bestcost = new_cost

                    # Construct a solution and send it to output pipe
                    solution = Solution( bestcost )
                    for node in bestroute:
                        solution.node_list.append( copy.deepcopy(node) )
                    solution_pipe.send( solution )
                    tracepoint_pipe.send( Tracepoint( time.process_time() - start_time, bestcost ) )
        route_matrix = bestroute

    exit( 0 ) # Exit process since all possible greedy startpoints have been hill-climbed.

def printmat(mat):
    for i in range(0,len(mat)):
        for j in range(0,len(mat)):
            print(mat[i,j].cost, end =" ")  
        print()    

def ls1( nodes , timeout : int,seed_num ):
    start_time = time.process_time()
    solution_read, solution_write = Pipe()
    tracepoint_read, tracepoint_write = Pipe()
    random.seed(seed_num)
    trace = Trace()
    mat = distance_calculator(nodes)
    start_nodes = []
    for i in range(0,len(nodes)):
        start_nodes.append(i)
    random.shuffle(start_nodes)

    p = Process( target = two_opt, args = (mat,nodes,start_nodes,tracepoint_write, solution_write ) ) 
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

