The TSP code package consists of 4 available algorithms, namely Branch-and-Bound, 2MST Approximation, 
2-OPT Hill Climb Local Search, and Simulated Annealing Local Search.

Each algorithm can be executed individually through the use of the tsp_main.py file.
The tsp_main.py file accepts up to 4 arguments through the use of input flags. The input
flags available consist of:
    -inst The data path of the .tsp file used for analysis.
    -alg  The algorithm type to execute with available choices being:
        LS1 - 2-OPT Local Search Hill Climbing algorithm
        LS2 - Simulated Annealing algorithm
        Approx - 2MST Approximation algorithm
        BnB - Branch and Bound algorithm
    -time The length in seconds that the algorithm may execute before reaching timeout
    -seed The integer used to seed the random number generator (Required when using Local Search)
The tsp_types.py file contains various classes and helper functions to make data passage between elements standard. 
The UnionFind.py file defines classes and helper functions used to implement a Union-Find data structure.
The run-main.py file is a script which is used to run the algorithms on all the input files.
The process-data.py file is a script which is used to generate comprehensive tables for the performance of the
algorithms which can be embedded into a TeX file.

With the exception of the run-main.py and process-data.py files all other files only have dependencies on the NumPy
library and the python standard library. The remaining files have dependencies on libraries which come standard
with most Python installations (i.e. Anaconda).

The algorithms proper are located in the tsp_approx.py, tsp_ls1.py, tsp_ls2.py, and tsp_bnb.py files. The general
structure for each of these files is an entrance function which will spawn  a timing process and spawn a new
process which runs the algorithm and communicates results using pipes. In such a manner the algorithm process can be
terminated precisely when the timeout is reached with no fear of losing results.

