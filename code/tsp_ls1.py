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
def greedy_heuristic(dist_matrix,index_start):
    initialdist_matrix = dist_matrix
    start_index = index_start#random.randint(0,dist_matrix.shape[0]-1)
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
            # TODO: instead, pass a list of flags into get_min_cost indicating which nodes have not been visited
            # and perform a single linear search which finds node s.t. cost is minimal AND it has not been visited
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
    # TODO: This loop does not consider flips which include endpoints
    for i in range(1,len(route_matrix)-1):
        for k in range(i+i,len(route_matrix)):
            improved_route = route_matrix[:]
            improved_route[i:k] = route_matrix[k-1:i-1:-1] #Here we will take the section to flip and flip it and replace the order.
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
    random.seed(seed_num)
    top_cost = np.inf
    top_route = []
    trace = Trace()
    starttime = time.time()
    mat = distance_calculator(nodes)
    start_nodes = []
    for i in range(0,len(nodes)):
        start_nodes.append(i)
    random.shuffle(start_nodes)

    for x in start_nodes:
        # TODO: Make a deepcopy of the matrix and pass it in on line 97, that way you won't have to recalc at line 105
        route,total_cost = greedy_heuristic(mat,x)
        if total_cost < top_cost:
            top_cost = total_cost
            top_route = route
            trace.add_tracepoint(time.time() - starttime,total_cost)
        #print(route,total_cost)
        #trace.add_tracepoint(time.time() - starttime,total_cost)
        improving = True
        mat = distance_calculator(nodes)
        if time.time()-starttime > timeout:
            # TODO: is it sufficient just to return the solution? if greedy_heuristic returned a better total_cost
            # a trace was already added in line 101 and top_cost was updated so the condition on next line is always 0?
            if total_cost < top_cost:
                trace.add_tracepoint(time.time() - starttime,total_cost)
                return Solution( total_cost, top_route), trace
            else:
                return Solution(top_cost, top_route), trace
        while improving:
            if time.time()-starttime > timeout:
                if total_cost < top_cost:
                    trace.add_tracepoint(time.time() - starttime,total_cost)
                    return Solution( total_cost, route), trace
                else:
                    return Solution(top_cost, top_route), trace      
            improving, route, total_cost = two_opt(route,mat,total_cost)
            if total_cost < top_cost:
                top_cost = total_cost
                top_route = route
                trace.add_tracepoint(time.time() - starttime,total_cost)              #print(route,total_cost)
    # TODO: can the return on the next line actually ever be hit?
    return Solution( top_cost, top_route), trace

