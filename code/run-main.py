import glob
import os
from pathlib import Path
from inspect import getsourcefile
import subprocess

# Script entry point
if __name__ == '__main__':
    code_dir = Path(getsourcefile(lambda: 0)).parent # Get absolute path to this script and remove filename
    top_dir = code_dir.parent # Get parent directory to where the executable resides
    input_dir = top_dir / 'data' # Construct path to directory with input files
    output_dir =  top_dir / 'output' # Construct path to output directory
    Path.mkdir(output_dir, exist_ok=True) # Make the directory if it doesn't already exist

    # Get a list of input files in the input directory
    input_filepaths = glob.glob(os.path.join(input_dir, '*.tsp'))

    # alg_list = ['Approx', 'BnB', 'LS1', 'LS2']
    alg_list = ['LS1', 'LS2']

    # Run local search algorithms on each input file
    for input_filepath in input_filepaths:
        for alg  in alg_list:
            for seed in range(10):
                args = [ 'python', str(code_dir / 'tsp_main.py'), '-inst', input_filepath, '-alg', alg, '-time', '20', '-seed', '{}'.format(seed)]
                p = subprocess.Popen( args )
                p.wait( 25 ) # Wait for the process to finish before moving on

    # Run Approximation algorithm on each input file
    for input_filepath in input_filepaths:
        alg = 'Approx'
        args = [ 'python', str(code_dir / 'tsp_main.py'), '-inst', input_filepath, '-alg', alg, '-time', '20']
        p = subprocess.Popen( args )
        p.wait( 25 ) # Wait for the process to finish before moving on

    # Run Branch and Bound algorithm on each input file
    for input_filepath in input_filepaths:
        alg = 'BnB'
        args = ['python', str(code_dir / 'tsp_main.py'), '-inst', input_filepath, '-alg', alg, '-time', '600']
        p = subprocess.Popen(args)
        p.wait(605)  # Wait for the process to finish before moving on

    exit( 0 )