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
            if x == y:
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

def calculate_route_cost(route,cost_matrix):
    cost = 0
    for i in range(0,len(route)-1):
        cost += cost_matrix[route[i],route[i+1]].cost
    return cost


def two_opt(route_matrix,dist_matrix,cost):
    bestroute = route_matrix
    improvement = False
    for i in range(1,len(route_matrix)-2):
        for k in range(i+i,len(route_matrix)):
            improved_route = route_matrix[:]
            improved_route[i:k] = route_matrix[k-1:i-1:-1]
            new_cost = calculate_route_cost(improved_route,dist_matrix)
            if new_cost < calculate_route_cost(bestroute,dist_matrix):
                bestroute = improved_route
                improvement = True
    route_matrix = bestroute
    return improvement, route_matrix, calculate_route_cost(route_matrix,dist_matrix)

def printmat(mat):
    for i in range(0,len(mat)):
        for j in range(0,len(mat)):
            print(mat[i,j].cost, end =" ")  
        print()    

def ls1( nodes , timeout : int,seed_num ):
    trace = Trace()
    starttime = time.time()
    mat = distance_calculator(nodes)
    route,total_cost = greedy_heuristic(mat,seed_num)
    print(route,total_cost)
    trace.add_tracepoint(round(time.time() - starttime,2),total_cost)
    improving = True
    mat = distance_calculator(nodes)
    while improving:
        improving, route, total_cost = two_opt(route,mat,total_cost)
        print(route,total_cost)
    return Solution( total_cost, route), trace

