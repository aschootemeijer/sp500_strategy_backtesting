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


def format_perc( perc ):
    #symbol = '📈' if perc >= 0 else '📉'
    symbol = '🟢' if perc >= 0 else '🔴'
    return f"{symbol} {perc:.1f}%" 
def add_perc_column( d, increase_factor_col_name ):
    perc = 100 * (d[ increase_factor_col_name ] - 1)
    d[ 'perc_since_trigger' ] = perc.apply( format_perc )
    return d


if __name__ == "__main__":
    d = pd.DataFrame( {'incr_frac':[ 0.96, 1.7], 'ticker':['NVDA', 'KLAC']} )
    print(  d  )
    d = add_perc_column( d,'incr_frac' )
    print(  d  )
