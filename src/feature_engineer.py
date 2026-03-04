import pandas as pd

def feature_engineer_data( d,momentum_interval_in_days ):
    d = d.copy()
    d['Close_max'] = d['Close'].cummax()
    d['Close_div_close_max'] = d['Close'] / d['Close_max']
    ''' FOR MOMENTUM STRATEGY '''
    for i in [momentum_interval_in_days,2*momentum_interval_in_days]:
        d[f'Close_dmin{i}'] = d['Close'].copy()
        d[f'Close_dmin{i}'] = d[f'Close_dmin{i}'].shift(i)
    return d


