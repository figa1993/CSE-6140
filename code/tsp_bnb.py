from tsp_types import Solution
from tsp_types import Trace

def bnb( nodes , timeout : int ):
    trace = Trace()
    trace.add_tracepoint( 0.234, 5 )
    trace.add_tracepoint( 2.4545, 89 )
    return Solution( 0, [ 0, 1, 2 ] ), trace