#-------------------------------------2-Opt Hill Climb Local Search Algorithm-----------------------------------------#
#The 2-Opt Local Search Hill Climb algorithm considers each possible Greedy route in random order as a starting       #
#point for the 2-opt exchange hill climb. Once initialized with a given greedy solution, the algorithm considers      #
#all possible 2-opt neighbors, updating the current optimal value if the current 2-Opt exchange provides a better     #
#solution than the current. Due to the finite number of combinations considered by the initial algorithm steps, the   #
#user has the option to include a randomized 2-Opt Exchange portion that will run and attempt to improve on the       #
#current optimal until the timeout has reached. This gives the algorithm flexability to either run and return a       #
#relatively low error answer in a short period of time, or use all of the time available to continue to search for a  # 
#more optimal route.                                                                                                  #
#---------------------------------------------------------------------------------------------------------------------#                                                                                                #
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

#Function to calculate the distance between each location in the problem
def distance_calculator(nodes):
    num_locs = len(nodes)
    mat = np.empty((num_locs,num_locs), dtype=Edge)
    for x in range(num_locs):
        for y in range(num_locs):
            mat[x,y] = Edge(nodes[x],nodes[y])
            if x == y:
                mat[x,y].cost = np.inf
    return mat

#Function to determine the closest location to the current that is still available
def get_min_cost(dest_group,rem_nodes):
    min_cost = np.inf
    min_index = np.inf
    for i in range (0,dest_group.shape[0]):
        if (dest_group[i].cost < min_cost) and rem_nodes[i] == 1:
            min_cost = dest_group[i].cost
            min_index = i
    return min_cost, min_index

#Function that returns a greedy route using the given starting node.
def greedy_heuristic(dist_matrix,index_start):
    initialdist_matrix = dist_matrix
    start_index = index_start
    total_cost = 0
    route = []
    rem_nodes = np.ones(dist_matrix.shape[0])
    rem_nodes[start_index] = 0
    route.append(start_index)
    while rem_nodes.any(): #while there are still unused locations keep updating the route
        dist,next_hop = get_min_cost(dist_matrix[start_index,],rem_nodes)
        route.append(next_hop)
        start_index = next_hop
        rem_nodes[next_hop] = 0
        total_cost += dist
    total_cost += initialdist_matrix[route[len(route)-1],route[0]].cost
    route.append(route[0])
    return route,total_cost

#Function to calculate a given route cost.
def calculate_route_cost(route,cost_matrix):
    cost = 0
    for i in range(0,len(route)-1):
        cost += cost_matrix[route[i],route[i+1]].cost
    return cost

#2-Opt exchange algorithm which uses Greedy as an initial solution 
def two_opt(nodes, tracepoint_pipe : Pipe, solution_pipe : Pipe, random_sample = True ):
    start_nodes = []
    for i in range(0,len(nodes)):
        start_nodes.append(i)
    random.shuffle(start_nodes)
    start_time = time.process_time()
    dist_matrix = distance_calculator(nodes)
    bestroute = None
    bestcost = np.inf
    for x in start_nodes:
        greedy_route,_ = greedy_heuristic(dist_matrix,x)
        route_matrix = greedy_route # Use greedy heuristic solution as the starting point
        for i in range(1,len(route_matrix)-1):
            for k in range(i+i,len(route_matrix)):
                improved_route = route_matrix[:]
                improved_route[i:k] = route_matrix[k-1:i-1:-1] #Here we will take the section to flip and flip it and replace the order.
                new_cost = calculate_route_cost(improved_route,dist_matrix)
                if new_cost < bestcost:
                    bestroute = improved_route
                    bestcost = new_cost
                    # Construct a solution and send it to output pipe
                    solution = Solution( bestcost )
                    for v in range( 0, len(bestroute) ):
                        node = bestroute[v]
                        solution.node_list.append( copy.deepcopy(node) )
                    solution_pipe.send( solution )
                    tracepoint_pipe.send( Tracepoint( time.process_time() - start_time, bestcost ) )
        route_matrix = bestroute
    if random_sample:
        while 1:
            random.shuffle(start_nodes)
            route_matrix = start_nodes
            for i in range(1,len(route_matrix)-1):
                for k in range(i+i,len(route_matrix)):
                    improved_route = route_matrix[:]
                    improved_route[i:k] = route_matrix[k-1:i-1:-1] #Here we will take the section to flip and flip it and replace the order.
                    new_cost = calculate_route_cost(improved_route,dist_matrix)
                    if new_cost < bestcost:
                        bestroute = improved_route
                        bestcost = new_cost
                        # Construct a solution and send it to output pipe
                        solution = Solution( bestcost )
                        for v in range( 0, len(bestroute) ):
                            node = bestroute[v]
                            solution.node_list.append( copy.deepcopy(node) )
                        solution_pipe.send( solution )
                        tracepoint_pipe.send( Tracepoint( time.process_time() - start_time, bestcost ) )
            route_matrix = bestroute
    else:
        return solution

#Helper function to print a numpy matrix for debugging
def printmat(mat):
    for i in range(0,len(mat)):
        for j in range(0,len(mat)):
            print(mat[i,j].cost, end =" ")  
        print()    

#Main function which controls the process timing and gathers data using Pipes
def ls1( nodes , timeout : int,seed_num):
    start_time = time.process_time()
    solution_read, solution_write = Pipe()
    tracepoint_read, tracepoint_write = Pipe()
    random.seed(seed_num)
    solution = Solution()
    trace = Trace()
    p = Process( target = two_opt, args = (nodes,tracepoint_write, solution_write) )
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

