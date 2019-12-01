import matplotlib
import os
import sys 

def qrtd(city_algorithm_time : str,directory : str):
    #input for this will be the city, algorithm, and time that we are looking at 
    keyword = city_algorithm_time
    for fname in os.listdir('output'):
        if keyword in fname:
            if '.trace' in fname:
                print(fname, "has the keyword")
    #with open( args.inst, newline='' ) as csvfile:

def sqd():
    pass 

def box_plot():
    pass

if __name__== "__main__":
  qrtd(sys.argv[1],sys.argv[2])