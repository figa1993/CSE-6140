from tsp_types import Solution
from tsp_types import Trace
from tsp_types import Node
from tsp_types import Edge
from tsp_types import Tracepoint
import random
import numpy as np
import math
import time
from multiprocessing import Process, Pipe, Queue

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

def calculate_route_cost(route,cost_matrix):
    cost = 0
    for i in range(0,len(route)-1):
        cost += cost_matrix[route[i],route[i+1]].cost
    return cost

def printmat(mat):
    for i in range(0,len(mat)):
        for j in range(0,len(mat)):
            print(mat[i,j].cost, end =" ")  
        print()   

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
        dist,next_hop = get_min_cost(dist_matrix[start_index,],rem_nodes)
        route.append(next_hop)
        start_index = next_hop
        rem_nodes[next_hop] = 0
        total_cost += dist
    total_cost += initialdist_matrix[route[len(route)-1],route[0]].cost
    route.append(route[0])
    return route,total_cost    

def accep_criteria(neighbor_route,current_route,cost_matrix,temperature):
    neighbor_route_cost = calculate_route_cost(neighbor_route,cost_matrix)
    current_route_cost = calculate_route_cost(current_route,cost_matrix)
    if neighbor_route_cost < current_route_cost:
        return neighbor_route,calculate_route_cost(neighbor_route,cost_matrix)
    else:
        probability = math.exp(-(neighbor_route_cost - current_route_cost) / temperature)
        if probability >= random.random():
            return neighbor_route,calculate_route_cost(neighbor_route,cost_matrix)
    return current_route,current_route_cost
    
def anneal_route(nodes,start_nodes,initial_T,ending_T,cost_matrix, tracepoint_pipe : Pipe, solution_pipe : Pipe):
    start_time = time.process_time()
    a = .995 #cooling constant
    mat = distance_calculator(nodes)
    initial = 1
    while 1:
        for x in start_nodes:
            temperature = initial_T
            greedy_route,greedy_total_cost = greedy_heuristic(mat,x)
            if initial == 1:
                best_route = greedy_route
                best_cost = greedy_total_cost
                initial = 0
            num_cities = len(greedy_route)-1
            current_route = greedy_route
            while temperature >= ending_T:
                adder_rand = random.randint(2,num_cities-1)
                left_rand = random.randint(1,num_cities-adder_rand)
                neighbor_route = current_route[:]
                neighbor_route[left_rand:(left_rand + adder_rand)] = reversed(neighbor_route[left_rand:(left_rand + adder_rand)])
                current_route,current_cost = accep_criteria(neighbor_route,current_route,cost_matrix,temperature)
                if current_cost < best_cost:
                    best_cost = current_cost
                    best_route = current_route
                    print("Optimal Updated by Annealing")
                    solution_pipe.send(Solution( best_cost, best_route))
                    tracepoint_pipe.send( Tracepoint( time.process_time() - start_time, best_cost ) )
                if  current_cost-best_cost > best_cost*.5:
                    print("Resetting Annealing")
                    current_route = greedy_route
                    current_cost = greedy_total_cost
                    temperature = initial_T
                temperature = temperature*a
    solution_pipe.send(Solution( best_cost, best_route))
    tracepoint_pipe.send( Tracepoint( time.process_time() - start_time, best_cost ) )
    

def ls2( nodes , timeout : int,seed_num ): #Here we will implement the Simulated Annealing Algorithm
    start_time = time.time()# Get current uptime in secconds
    solution_read, solution_write = Pipe()
    tracepoint_read, tracepoint_write = Pipe()
    random.seed(seed_num)
    ending_temp = random.random()
    initial_temp = random.randrange(len(nodes))
    trace = Trace()
    mat = distance_calculator(nodes)
    start_nodes = []
    for i in range(0,len(nodes)):
        start_nodes.append(i)
    random.shuffle(start_nodes) 
    p = Process( target = anneal_route, args = (nodes,start_nodes,initial_temp,ending_temp,mat,tracepoint_write, solution_write ) ) 
    p.start() # Start the process
    while( time.time()-start_time < timeout ):
        if solution_read.poll(timeout - ( time.time() - start_time )) and\
                tracepoint_read.poll(timeout - ( time.time() - start_time )) :
            # Block until a solution is available or timeout
            solution = solution_read.recv( )
            
            # Receive corresponding tracepoint and append
            tracepoint = tracepoint_read.recv()
            trace.add_tracepoint(float(tracepoint.time),tracepoint.quality)
            print("New Best Value of",tracepoint.quality,"found")
            print("Time Elapsed: ",time.time()-start_time)
        else:
            # Timeout has occured break out of loop
            break
    p.join(0)
    print("Algorithm Finished in",time.time()-start_time,"seconds")
    p.terminate()
    #greedyroute,greedytotal_cost = greedy_heuristic(mat,0)
    #route, total_cost = anneal_route(greedyroute,greedytotal_cost,initial_temp,ending_temp,mat)
    return solution, trace







        
        