The TSP code package consists of 4 available algorithms, namely Branch-and-Bound, 2MST Approximation, 
2-OPT Hill Climb Local Search, and Simulated Annealing Local Search that can be executed through the use of 
the tsp_main.py file. The tsp_main.py file accepts up to 5 arguments through the use of input flags. The input 
flags available consist of:
    -inst The data path of the .tsp file used for analysis.
    -alg  The algorithm type to execute with available choices
        LS1 - 2-OPT Local Search Hill Climbing algorithm
        LS2 - Simulated Annealing algorithm
        Approx - 2MST Approximation algorithm
        BnB - Branch and Bound algorithm
    -time The length in seconds that the algorithm may execute before reaching timeout
    -seed The integer used to seed the random number generator (Required when using Local Search)
    -random An optional parameter that may be used when executing the 2-OPT Local Search Algorithm 
            which gives the user the option to run addition random starting points until timeout.
The tsp_types.py file contains various classes and helper functions to make data passage between elements standard. 
All libraries used throughout the project can be found in a standard anaconda 
distribution of python 