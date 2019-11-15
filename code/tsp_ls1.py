from tsp_types import Solution
from tsp_types import Trace
from tsp_types import Node
from tsp_types import Edge
import random
import numpy as np
import math
import time

def distance_calculator(nodes):
    num_locs = len(nodes)
    mat = np.empty((num_locs,num_locs), dtype=Edge)
    for x in range(num_locs):
        for y in range(num_locs):
            mat[x,y] = Edge(nodes[x],nodes[y])
            if mat[x,y].cost == float(0):
                mat[x,y].cost = np.inf
    return mat

def get_min_cost(dest_group):
    min_cost = np.inf
    min_index = np.inf
    for i in range (0,dest_group.shape[0]):
        if dest_group[i].cost < min_cost:
            min_cost = dest_group[i].cost
            min_index = i
    return min_cost, min_index

#This will solve a greedy problem to give us a place to start
def greedy_heuristic(dist_matrix,seed_num):
    random.seed(seed_num)
    initialdist_matrix = dist_matrix
    start_index = random.randint(0,dist_matrix.shape[0])
    total_cost = 0
    route = []
    rem_nodes = np.ones(dist_matrix.shape[0])
    rem_nodes[start_index] = 0
    route.append(start_index)
    while rem_nodes.any(): #while there are still unused locations
        dist,next_hop = get_min_cost(dist_matrix[start_index,])
        if rem_nodes[next_hop] == 1:
            route.append(next_hop)
            start_index = next_hop
            rem_nodes[next_hop] = 0
            total_cost += dist
        else:
            dist_matrix[start_index,next_hop].cost = np.inf
    total_cost += initialdist_matrix[route[len(route)-1],route[0]].cost
    route.append(route[0])
    return route,total_cost

def two_opt(route_matrix,dist_matrix,cost):
    pass

def ls1( nodes , timeout : int,seed_num ):
    starttime = time.time()
    mat = distance_calculator(nodes)
    route,total_cost = greedy_heuristic(mat,seed_num)
    print(time.time() - starttime)
    print(route,total_cost)
    two_opt(route,mat,total_cost)
    trace = Trace()
    trace.add_tracepoint( 0.234, 5 )
    trace.add_tracepoint( 2.4545, 89 )
    return Solution( 0, [ 0, 1, 2 ] ), trace

