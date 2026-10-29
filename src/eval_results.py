import numpy as np
import pandas as pd
from scipy import stats
from scipy.optimize import brentq


def calc_xirr( dates, cashflows, use_utc ):
    """
    (X)IRR: Internal Rate of Return (or annual return)
    XNPV:   eXtended Net Present Value. Essentially uses time difference between cashflows.
    The correct rate (annual return) is the one for which the sum of the XNPV is zero
    """
    if len( dates ) == 0:   # no stocks were bought, so there is no return to calculate
        return None
    #dates = pd.to_datetime( dates )
    dates     = pd.to_datetime( dates, utc=use_utc )
    years     = np.array( (dates - min(dates)).days ) / 365.25   # time of each cashflow, in years after the first buy
    cashflows = np.array( cashflows, dtype=float )
    def xnpv( rate ):
        return np.sum( cashflows / (1 + rate)**years )
    # check -99% to +1000% per year in steps of 1%. At the correct rate, XNPV goes from positive to negative.
    # If buys are years apart, XNPV can also cross zero at very negative rates, where the latest buys dominate
    # the sum. Those crossings have no meaning, so we take the highest crossing.
    rates   = np.linspace( -0.99, 10, 1100 )
    values  = np.array([ xnpv(r) for r in rates ])
    crosses = np.where( (values[:-1] > 0) & (values[1:] <= 0) )[0]
    if len( crosses ) == 0:   # no solution between -99% and +1000% per year
        return None
    i = crosses[-1]
    return np.round( brentq( xnpv, rates[i], rates[i+1] ) * 100, 1 )   # brentq finds the exact rate within that 1% step

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
