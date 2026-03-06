import numpy as np
from scipy import stats

def calc_avg_yrly_incr(periods, value_rats):
    if not periods: return 0, 0
    weighted_avg_ratio = sum(p * r for p, r in zip(periods, value_rats)) / sum(periods)
    avg_period = sum(periods) / len(periods)
    time_avg_yrly_incr = np.round(100 * (weighted_avg_ratio ** (1 / avg_period) - 1), 1)
    avg_total_incr = np.round((np.mean(value_rats) - 1) * 100, 1)
    return time_avg_yrly_incr, avg_total_incr


def calc_p_value( strategy_value_rats, control_value_rats ):
    lala = stats.ks_2samp( strategy_value_rats, control_value_rats )
    return lala.pvalue

#def calc_avg_yrly_incr( periods, value_rats ): # had issues
#    sums               = sum( i[0]*i[1] for i in zip( periods,value_rats ) )
#    time_avg_value_rat = sums /sum( periods )
#    avg_period         = np.mean( periods )
#    time_avg_yrly_incr = np.round( 100*( time_avg_value_rat ** (1/avg_period) -1 ), 1 )
#    return time_avg_yrly_incr, np.round( (time_avg_value_rat-1)*100., 1 )
