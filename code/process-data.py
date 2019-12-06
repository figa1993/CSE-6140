import glob
import os
from pathlib import Path
from inspect import getsourcefile
import pandas as pd
import csv

def calculate_relative_error( optimal, value ):
    value = int(value)
    return '{:0.4f}'.format(abs( optimal - value )/optimal)

# Script entry point
if __name__ == '__main__':
    code_dir = Path(getsourcefile(lambda: 0)).parent # Get absolute path to this script and remove filename
    top_dir = code_dir.parent # Get parent directory to where the executable resides
    input_dir =  top_dir / 'output' # Construct path to output directory
    output_dir = top_dir / 'report' # Construct path to output directory

    Path.mkdir(output_dir, exist_ok=True) # Make the directory if it doesn't already exist

    # Get a list of input files in the input directory
    input_filepaths = glob.glob(os.path.join(input_dir, '*.trace'))

    # Create a dictionary mapping the instance to its optimal value
    instance_optimum_map =\
    {
        'Atlanta' : 2003763,
        'Berlin' : 7542,
        'Boston' : 893536,
        'Champaign' :  52643,
        'Cincinnati' : 277952,
        'Denver' : 100431,
        'NYC' : 1555060,
        'Philadelphia' : 1395981,
        'Roanoke' : 655454,
        'SanFrancisco' : 810196,
        'Toronto' : 1176151,
        'UKansasState' : 62962,
        'UMissouri' : 132709
    }


    # Create a dataframe which will represent the table. Headers are metrics, rows are metrics
    # df = pd.DataFrame( [{'Time[s]' : 0, 'Solution Quality' : 1, 'Relative Error' : 2}], index = ['Cincinnati'],  columns = ['Time[s]', 'Solution Quality', 'Relative Error'] )
    # df.name = 'title'

    # df = pd.DataFrame( columns=['Instance', 'Time[s]', 'Solution Quality', 'Relative Error'])
    # df.loc[0] = {'Cincinatti' : [0, 1, 2]}

    data = { 'Cincinatti' : [0, 1, 2] }
    df = pd.DataFrame.from_dict( data, orient='index', columns=['Time[s]', 'Solution Quality', 'Relative Error'])
    df.index.name = 'Instance'

    approx_dict = {}
    ls1_dict = {}
    ls2_dict = {}
    bnb_dict = {}

    alg_dict = \
    {
        'Approx' : approx_dict,
        'LS1' : ls1_dict,
        'LS2' : ls2_dict,
        'BnB' : bnb_dict
    }

    # Read in each trace file
    for input_filepath  in input_filepaths:
        with open(input_filepath, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            # Read the rows in file
            tracepoints = []
            for row in reader:
                tracepoints.append( row )

        # The last row has the data needed
        print( input_filepath )
        result = tracepoints[-1]

        filename = Path(input_filepath).stem
        file_descriptors = filename.split('_')
        instance = file_descriptors[0]
        alg = file_descriptors[1]

        runtime = result[0]
        quality = result[1]
        rel_err = calculate_relative_error( instance_optimum_map[instance], quality )

        if instance in alg_dict[alg]:
            alg_dict[alg][instance].append( [float(runtime), int(quality)] )
        else:
            alg_dict[alg][instance] = [ [ float(runtime), int(quality)] ]

    for item in alg_dict.items():

        # Average results for instances which have several results for the same algorithm
        # ASSUMPTION IS EVERY ALGORITHM TRACE IS FOR THE SAME CUTOFF TIME!!
        for instance_items in alg_dict[item[0]].items():
            average = [0., 0]
            for results in instance_items[1]:
                average[0] += results[0]
                average[1] += results[1]
            average[0] = average[0]/len(instance_items[1])
            average[1] = average[1] // len(instance_items[1]) # Integer division on quality
            average.append( calculate_relative_error( instance_optimum_map[instance_items[0]] , average[1] ) )
            # Convert runtime and quality to strings with appropriate digits
            average[0] = '{:0.2f}'.format(average[0])
            average[1] = str( average[1] )

            alg_dict[item[0]][instance_items[0]] = average # Reset the value in the dictionary to the list of results

        output_filepath = output_dir / 'comprehensive_table_{}.tex'.format( item[0] )
        df = pd.DataFrame.from_dict( item[1], orient= 'index', columns=['Time[s]', 'Solution Quality', 'Relative Error'] )
        df.index.name = 'Instance'
        with open(output_filepath, 'w') as output_file:
            # output_file.write(df.to_latex())
            # output_file.write(df.to_latex().replace('\\toprule', '\\toprule\n\caption{{ {} Algorithm Performance Table }}\\\\'.format(item[0]) ) )
            output_file.write('\\begin{table}\n')
            output_file.write('\caption{{ {} Algorithm Performance Table }}\n'.format(item[0]))
            output_file.write(df.to_latex())
            output_file.write('\\end{table}\n')

    # output_filepath = output_dir / 'comprehensive_table.tex'
    # with open(output_filepath, 'w') as output_file:
    #     output_file.write( df.to_latex() )



    exit( 0 )