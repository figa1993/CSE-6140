from matplotlib import pyplot
import numpy as np
import os
import sys 
import csv

class runtime_data():
    __slots__ = 'runtime','quality','success'
    def __init__(self,runtime,quality):
        self.runtime = runtime
        self.quality = quality
        self.success = False


def qrtd(city_algorithm_time : str,directory : str,optimal_value : int,time_limit : str):
    #input for this will be the city, algorithm, and time that we are looking at 
    keyword = city_algorithm_time
    dataarray = []
    qualarray = [.032,.035,.038]
    for fname in os.listdir('output'):
        if keyword in fname:
            if '.trace' in fname: #loop through all the associated trace files
                print(fname, "has the keyword")
                with open( "output/"+fname, newline='' ) as csvfile:
                    reader = csv.reader( csvfile, delimiter=' ' )
                    for row in reader:
                        timeval = row
                timeval = timeval[0]
                timeval = timeval.split(',')
                dataarray.append(runtime_data(float(timeval[0]),int(timeval[1])))
    #fig = pyplot.figure()
    for qual in qualarray:
        #print(qual)
        xplot = []
        yplot = []
        k = 0
        for x in dataarray:
            k += 1
            if ((x.quality - int(optimal_value)) / int(optimal_value)) >= qual:
                x.success = False
            else:
                x.success = True
                xplot.append(x.runtime)
                xplot.sort()
                yplot.append(k)
        #print(xplot)
        yplot[:] = [g / k for g in yplot]
        print(yplot)
        print(xplot)
        pyplot.plot(xplot,yplot,label = str(qual))
    pyplot.legend()
    pyplot.show()

            #print(x.success,x.quality,x.runtime)
        



def sqd(city_algorithm : str,directory : str,optimal_value : int,time_limit : str):
    time_array = [20,10]
    timedataarray = []
    timearray =  time_array
    for times in timearray:
        dataarray = []
        keyword = city_algorithm + "_" + str(times)
        for fname in os.listdir('output'):
            if keyword in fname:
                if '.trace' in fname: #loop through all the associated trace files
                    print(fname, "has the keyword")
                    with open( "output/"+fname, newline='' ) as csvfile:
                        reader = csv.reader( csvfile, delimiter=' ' )
                        for row in reader:
                            timeval = row
                    timeval = timeval[0]
                    timeval = timeval.split(',')
                    dataarray.append(runtime_data(float(timeval[0]),int(timeval[1])))
        timedataarray.append(dataarray)
    #fig = pyplot.figure()
    maxqual = .08
    index = 0
    for time in timearray:
        #print(qual)
        xplot = []
        yplot = []
        k = 0
        dataarray = timedataarray[index]
        for x in dataarray:
            k += 1
            if ((x.quality - int(optimal_value)) / int(optimal_value)) >= maxqual:
                x.success = False
            else:
                x.success = True
                xplot.append((x.quality - int(optimal_value)) / int(optimal_value))
                xplot.sort()
                yplot.append(k)
        #print(xplot)
        yplot[:] = [g / k for g in yplot]
        print(yplot)
        print(xplot)
        pyplot.plot(xplot,yplot,label = str(time) + " seconds")
        index += 1
    pyplot.legend()
    pyplot.title('Solution Quality Distributions')
    pyplot.show()

def box_plot():
    pass

if __name__== "__main__":
  sqd(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
  #qrtd(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])