import os
import sys
import csv
import numpy as np
import argparse

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