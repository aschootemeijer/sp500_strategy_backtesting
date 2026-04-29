import numpy as np
import pandas as pd
from scipy import stats
from scipy.optimize import newton


def calc_xirr( dates, cashflows ):
    """
    (X)IRR: Internal Rate of Return (or annual return)
    XNPV:   eXtended Net Present Value. Essentially uses time difference between cashflows.
    The correct rate (annual return) is the one for which the sum of the XNPV is zero
    """
    dates = pd.to_datetime( dates )
    start_date = min(dates)
    print( '\nDATES',dates )
    print( '\nDAYS', (dates-start_date).days )
    print( '\nCASHFLOWS', cashflows )
    def xnpv(rate, cashflows, dates):
        start_date = min(dates)
        return sum([cf / (1 + rate)**((d - start_date).days / 365.25) for cf, d in zip(cashflows, dates)])
    # Newton-Raphson method to find rate at which XNPV is 0
    try:
        return np.round(newton(lambda r: xnpv(r, cashflows, dates), 0.1) * 100, 1)
    except RuntimeError:
        return 0.0


def _kutversie_calc_xirr( dates, cashflows ):
    """
    (X)IRR: Internal Rate of Return (or annual return)
    XNPV:   eXtended Net Present Value. Essentially uses time difference between cashflows.
    The correct rate (annual return) is the one for which the sum of the XNPV is zero
    """
    dates = pd.to_datetime( dates )
    days_from_start = ( dates - min(dates) ).days.tolist()
    print( 'DATES\n',dates )
    print( 'DAYS\n', days_from_start )
    #print( 'DAYS\n', (dates - start_date).days )

    def xnpv(rate, cashflows, days_from_start_f):
        #start_date = min(dates)
        return sum([cf / (1 + rate)**( d / 365.25) for cf, d in zip(cashflows, days_from_start_f)])
    # Newton-Raphson method to find rate at which XNPV is 0
    try:
        return np.round(newton(lambda r: xnpv(r, cashflows, days_from_start), 0.1) * 100, 1)
    except RuntimeError:
        return 0.0

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
