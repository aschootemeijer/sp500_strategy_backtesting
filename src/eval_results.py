import numpy as np

def calc_avg_yrly_incr( periods, value_rats ):
    sums               = sum( i[0]*i[1] for i in zip( periods,value_rats ) )
    time_avg_value_rat = sums /sum( periods )
    avg_period         = np.mean( periods )
    time_avg_yrly_incr = np.round( 100*( time_avg_value_rat ** (1/avg_period) -1 ), 1 )
    return time_avg_yrly_incr, np.round( (time_avg_value_rat-1)*100., 1 )

#def calc_avg_yrly_incr( periods, value_rats ):
#    avg_value_rat      = np.mean( value_rats )
#    avg_period         = np.mean( periods )
#    time_avg_yrly_incr = np.round( 100*( avg_value_rat ** (1/avg_period) -1 ), 1 )
#    return time_avg_yrly_incr
