from inspect import getsourcefile
import os
from pathlib import Path
import sys
import csv
import numpy as np
import argparse
from collections import deque

from tsp_bnb import bnb
from tsp_ls1 import ls1
from tsp_ls2 import ls2
from tsp_approx import approx

from tsp_types import Node
from tsp_types import Solution

def write_solution_to_file( output_filepath, solution : Solution ):
    with open( output_filepath, 'w', newline='' ) as csvfile:
        writer = csv.writer( csvfile, delimiter=',' )
        writer.writerow( [solution.quality] )
        writer.writerow( solution.node_list )

def write_trace_to_file( output_filepath, trace ):
    with open(output_filepath, 'w', newline='') as csvfile:
        writer = csv.writer( csvfile, delimiter=',' )
        writer.writerows( trace.tracepoints )

# Script entry point
if __name__ == '__main__':

    # Instantiate and configure argument parser object
    parser = argparse.ArgumentParser(description='TSP argument parser')
    parser.add_argument( '-inst', required=True )
    parser.add_argument( '-alg', required=True )
    parser.add_argument( '-time', required=True, type=int )
    parser.add_argument( '-seed', type=int )

    # Command argument parser to process command line arguments
    args = parser.parse_args()

    if (args.alg == 'LS1' or args.alg == 'LS2' ) and args.seed == None:
        sys.exit( "Usage: {}\t-seed parameter must be provided for -alg={}".format( parser.prog, args.alg ) )

    Nodes = []

    with open( args.inst, newline='' ) as csvfile:
        reader = csv.reader( csvfile, delimiter=' ' )
        inst_name = next( reader )[1] # Extract the name of the instance
        next( reader ) # Ignore line 2
        inst_dim = int( next( reader )[1] ) # Extract the number of points
        next( reader ) # Ignore line 4
        next( reader ) # Ignore line 5
        for i in range( inst_dim ):
            Nodes.append( Node( next(reader) ) )

    if args.alg == 'BnB':
        solution, trace = bnb( Nodes, args.time )
    if args.alg == 'LS1':
        solution, trace = ls1( Nodes, args.time ,args.seed)
    if args.alg == 'LS2':
        solution, trace = ls2( Nodes, args.time,args.seed )
    if args.alg == 'Approx':
        solution, trace = approx( Nodes, args.time )

    if args.seed != None:
        output_filename = '{}_{}_{}_{}'.format(Path(args.inst).stem, args.alg, args.time, args.seed)
    else:
        output_filename = '{}_{}_{}'.format(Path(args.inst).stem, args.alg, args.time)

    code_dir = Path(getsourcefile(lambda: 0)).parent # Get absolute path to this script and remove filename
    top_dir = code_dir.parent # Get parent directory to where the executable resides
    output_dir =  top_dir / 'output' # Construct path to output directory
    Path.mkdir(output_dir, exist_ok=True) # Make the directory if it doesn't already exist

    write_solution_to_file(  ( output_dir / output_filename ).with_suffix('.sol') , solution )
    write_trace_to_file( ( output_dir / output_filename ).with_suffix('.trace') , trace )

    exit( 0 )