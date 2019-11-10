import os
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
        sys.exit( "Usage: {}".format(parser.prog)+"\t-seed parameter must be provided for -alg={}".format(args.alg) )

    Nodes = deque()

    with open( args.inst, newline='' ) as csvfile:
        reader = csv.reader( csvfile, delimiter=' ' )
        inst_name = next( reader )[1] # Extract the name of the instance
        next( reader ) # Ignore line 2
        inst_dim = int( next( reader )[1] ) # Extract the number of points
        next( reader ) # Ignore line 4
        next( reader ) # Ignore line 5
        for i in range( inst_dim ):
            Nodes.append( Node( next(reader) ) )

    if args.alg == 'Bnb':
        bnb( Nodes, args.time )
    if args.alg == 'LS1':
        ls1( Nodes, args.time )
    if args.alg == 'LS2':
        ls2( Nodes, args.time )
    if args.alg == 'Approx':
        approx( Nodes, args.time )

    exit( 0 )
