#-------------------------------------Simulated Annealing Local Search Algorithm---------------------------------------#
#The Simulated Annealing algorithm using a Greedy route as a basis for the annealing process. Throughout the annealing #
#process, the probability is calculated using the acceptance criteria function, and then is compared to a randomly     #
#computer value to determine if a neighborhood which provides a less efficient route than the current best should be   #
#considered. This algorithm will continuously run until the timeout value is reached, continuously considering         #
#different Greedy routes as starting points. However the inherently random nature of the algorithm ensures that no two #
#iterations are the same even when using a set initial solution.                                                       #
#----------------------------------------------------------------------------------------------------------------------#    
from tsp_types import Solution
from tsp_types import Trace
from tsp_types import Node
from tsp_types import Edge
from tsp_types import Tracepoint
from tsp_ls1 import greedy_heuristic
from tsp_ls1 import distance_calculator
from tsp_ls1 import get_min_cost
from tsp_ls1 import calculate_route_cost
from tsp_ls1 import printmat
import random
import numpy as np
import math
import time
import copy
from multiprocessing import Process, Pipe, Queue  

#Function that performs the probability calculation if necessary, and returns the route and cost to consider based 
#on the acceptance criteria probability function.
def accep_criteria(neighbor_route,current_route,cost_matrix,temperature,current_route_cost):
    neighbor_route_cost = calculate_route_cost(neighbor_route,cost_matrix)
    if neighbor_route_cost < current_route_cost:
        return neighbor_route,calculate_route_cost(neighbor_route,cost_matrix)
    else:
        probability = math.exp(-(neighbor_route_cost - current_route_cost) / temperature)
        if probability >= random.random():
            return neighbor_route,calculate_route_cost(neighbor_route,cost_matrix)
    return current_route,current_route_cost
    
def anneal_route(nodes, tracepoint_pipe : Pipe, solution_pipe : Pipe, seed : int):
    start_time = time.process_time()
    random.seed( seed )
    cost_matrix = distance_calculator(nodes)
    ending_T = random.random()
    initial_T = random.randrange(len(nodes))
    start_nodes = []
    for i in range(0,len(nodes)):
        start_nodes.append(i)
    random.shuffle(start_nodes)
    a = .995 #cooling constant
    best_route = None
    best_cost = np.inf
    while 1:
        for x in start_nodes:
            temperature = initial_T

            greedy_route,greedy_total_cost = greedy_heuristic(cost_matrix,x)
            if greedy_total_cost < best_cost:
                best_cost = greedy_total_cost
                best_route = greedy_route
                # print( 'Optimal updated by greedy' )

                # Construct a solution and send it to output pipe
                solution = Solution(best_cost)
                for v in range(0, len(best_route) - 1):
                    node = best_route[v]
                    solution.node_list.append(copy.deepcopy(node))
                solution_pipe.send(solution)
                tracepoint_pipe.send(Tracepoint(time.process_time() - start_time, best_cost))

            num_cities = len(greedy_route)-1
            current_route = greedy_route
            current_cost = calculate_route_cost(current_route,cost_matrix)
            while temperature >= ending_T:
                adder_rand = random.randint(2,num_cities-1)
                left_rand = random.randint(1,num_cities-adder_rand)
                neighbor_route = current_route[:]
                neighbor_route[left_rand:(left_rand + adder_rand)] = reversed(neighbor_route[left_rand:(left_rand + adder_rand)])
                current_route,current_cost = accep_criteria(neighbor_route,current_route,cost_matrix,temperature,current_cost)
                if current_cost < best_cost:
                    best_cost = current_cost
                    best_route = current_route
                    # print("Optimal Updated by Annealing")

                    # Construct a solution and send it to output pipe
                    solution = Solution( best_cost )
                    for v in range( 0, len(best_route)-1 ):
                        node = best_route[v]
                        solution.node_list.append( copy.deepcopy(node) )
                    solution_pipe.send( solution )

                    tracepoint_pipe.send( Tracepoint( time.process_time() - start_time, best_cost ) )
                if  current_cost-best_cost > best_cost*.5:
                    # print("Resetting Annealing")
                    current_route = greedy_route
                    current_cost = greedy_total_cost
                    temperature = initial_T
                temperature = temperature*a
    exit( 0 )
    
#Main function which controls the process timing and gathers data using Pipes
def ls2( nodes , timeout : int,seed_num ): #Here we will implement the Simulated Annealing Algorithm
    start_time = time.process_time()# Get current uptime in secconds
    solution_read, solution_write = Pipe()
    tracepoint_read, tracepoint_write = Pipe()
    solution = Solution()
    random.seed(seed_num)
    trace = Trace()
    p = Process( target = anneal_route, args = (nodes,tracepoint_write, solution_write, seed_num ) )
    p.start() # Start the process

    # Have the thread spin so that it keeps track of time most accurately
    while( ( ( time.process_time()-start_time )  < timeout ) and p.is_alive() ):
        if solution_read.poll( 0 ) and tracepoint_read.poll( 0 ):
            # Blocking call which shouldn't block since poll conditions ensure data is available
            solution = solution_read.recv()
            trace.add_tracepoint( tracepoint_read.recv() ) # Receive corresponding tracepoint and append

    p.join( 0 ) # Join the subprocess which automatically closes the pipes
    if p.is_alive():
        p.terminate()

    return solution, trace