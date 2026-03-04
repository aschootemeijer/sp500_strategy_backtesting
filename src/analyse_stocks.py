import pandas as pd
import numpy as np

def get_index_of_buy_moment( d, strategy:str, momentum_factor, momentum_interval_in_days, frac_remaining, frac_bump ):
    if strategy == 'momentum':
        r = d[ (d['Close'] > momentum_factor*d[f'Close_dmin{momentum_interval_in_days}']) & (d['Close'] > momentum_factor**2*d[f'Close_dmin{2*momentum_interval_in_days}'])]
        r = r.index.min()
    if strategy == 'declining':
        r = d[ d.Close_div_close_max < frac_remaining ].index.min()
    if strategy == 'early_recovery':
        q = d[ d.Close_div_close_max < frac_remaining ].index.min()
        dq= d.loc[ q: ]
        dq= dq.copy()
        dq['Close_min'] = dq['Close'].cummin()
        dq['Close_div_close_min'] = dq['Close'] / dq['Close_min']
        r = dq[ dq.Close_div_close_min > frac_bump ].index.min()
    if strategy == 'all':
        r = np.random.choice( d.index )
    return r

def get_period_in_yr( df ):
    year_decimal = df.Date.dt.year + df.Date.dt.dayofyear / 365.25
    return year_decimal.iloc[-1] - year_decimal.iloc[0] 

def strategy_value_ratio_and_period_and_yearly_increase( d, r, track_time ):
    dr                      = d.loc[ r: ].copy()
    date0                   = dr.Date.iloc[0]
    dateend                 = date0 + pd.DateOffset( days=track_time )
    dr                      = dr[ (dr.Date >= date0) & (dr.Date <= dateend) ]
    period_in_yr            = get_period_in_yr( dr )
    value_ratio             = dr.Close.iloc[-1] / dr.Close.iloc[0]
    yearly_increase_in_perc = np.round( 100*( value_ratio ** (1 / period_in_yr) -1 ), 1 )
    return dr, value_ratio, period_in_yr, yearly_increase_in_perc, date0

def control_value_ratio_and_period_and_yearly_increase( d,track_time, date0, rand_offset ):
    rand_offset_in_d        = np.random.randint( -rand_offset, rand_offset+1 )
    date0                   = date0 + pd.Timedelta(  days=rand_offset_in_d )
    dateend                 = date0 + pd.DateOffset( days=track_time )
    if dateend > d.Date.max(): return None, None, None, None
    dr                       = d[ (d.Date >= date0) & (d.Date <= dateend) ]
    period_in_yr            = get_period_in_yr( dr )
    value_ratio             = dr.Close.iloc[-1] / dr.Close.iloc[0]
    yearly_increase_in_perc = np.round( 100*( value_ratio ** (1 / period_in_yr) -1 ), 1 )
    return dr, value_ratio, period_in_yr, yearly_increase_in_perc
