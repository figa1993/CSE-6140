import os
import sys
import csv
import numpy as np

# Script entry point
if __name__ == '__main__':
    args = sys.argv
    if len(args) < 7:
        sys.exit("Usage: {} -inst <filename> -alg [BnB|Approx|LS1|LS2] -time <cutoff_in_seconds> [-seed <random_seed>]".format(args[0]))

    input_filepath = sys.argv[2]
    alg_type = sys.argv[4]
    t_cutoff = sys.argv[6]

    if (alg_type == 'LS1' or alg_type == 'LS2' ) and len(args) < 9 :
        sys.exit( "Usage: {}".format(args[0])+"\t-seed parameter must be provided for -alg={}".format(args[4]) )