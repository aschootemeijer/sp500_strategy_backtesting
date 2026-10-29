import yfinance as yf
import pandas as pd
import requests
from io import StringIO
import datetime
import functools
import os

SP500_MONTHLY_FILE = '/mnt/c/Users/hp/Desktop/dinges/fin/experimenteren/tickerlists/sp500_monthly.csv'   # local file, not in the repository

def load_sp500_fromlist( years_back ):
    if not os.path.exists( SP500_MONTHLY_FILE ):   # e.g. for visitors who cloned the repository
        print( f'IMPORTANT. {SP500_MONTHLY_FILE} was not found: using the current S&P500 from Wikipedia instead (see README)' )
        return load_sp500( years_back )
    sp500_all = pd.read_csv( SP500_MONTHLY_FILE, parse_dates=['date'] )
    then  = datetime.datetime.now() - pd.offsets.DateOffset( years=years_back )
    sp500 = sp500_all[ (sp500_all.date.dt.year == then.year) & (sp500_all.date.dt.month == then.month) ] 
    return sp500.iloc[0,1:].dropna().tolist()
    
def read_sp500_wikipedia( ):
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    headers = {"User-Agent": "Mozilla/5.0"}    # else we get access denied
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return pd.read_html( StringIO( r.text ) )[0]

def load_sp500_dates_added( ):
    # date each current S&P500 stock was added to the index, e.g. dates_added['P'] -> 2026-09-21
    sp500 = read_sp500_wikipedia( )
    sp500['Symbol'] = sp500['Symbol'].str.replace( '.', '-', regex=False )   # Yahoo writes BRK.B as BRK-B
    return pd.to_datetime( sp500.set_index( 'Symbol' )['Date added'] )

def load_sp500( years_back ):
    sp500 = read_sp500_wikipedia( )
    #print( sp500.columns )
    #print( sp500[['Symbol','Security','GICS Sub-Industry']] )
    # these two lines below are to prevent bias: remove succesfull stocks that were added after years_back
    sp500['Date added'] = pd.to_datetime( sp500['Date added'] )
    sp500 = sp500[ sp500["Date added"].dt.year <= datetime.datetime.now().year - years_back ]
    stock_ticker_list = sp500['Symbol'].str.replace( '.', '-', regex=False ).tolist()   # Yahoo writes BRK.B as BRK-B
    return stock_ticker_list

def load_spX00( X00 = 500 ): # 400, 500, or 600
    url = f"https://en.wikipedia.org/wiki/List_of_S%26P_{X00}_companies"
    print( url )
    headers = {"User-Agent": "Mozilla/5.0"}    # else we get access denied
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    spX00 = pd.read_html( StringIO( r.text ) )[0]
    stock_ticker_list = spX00['Symbol'].str.replace( '.', '-', regex=False ).tolist()   # Yahoo writes BRK.B as BRK-B
    return stock_ticker_list 

def load_eur600( ):
    d = pd.read_csv( "/mnt/c/Users/hp/Desktop/dinges/fin/historical_data/eur600.csv" )
    #d = pd.read_csv( "/mnt/c/Users/hp/Desktop/dinges/fin/historical_data/ishares_eur600.csv" )
    print(d)
    return d["Ticker"].tolist()

@functools.lru_cache( maxsize=None )   # download each stock only once per session
def get_stock_data( stock_ticker, years_back ):
    try:
        d_all = yf.Ticker( stock_ticker )
        d     = d_all.history( period=f'{years_back}y', auto_adjust=True )
        if d is None or d.empty:
            return None
        d     = d.reset_index()
        if len(d) <= 1:
            return None
        return d
    except Exception:
        return None

    if len(d) <= 1:
        print( '!!!!!!!!! len(d) <= 1' )
        return


def get_stock_names( d, ticker_col_name ):
    stock_names = {}
    for ticker in d[ ticker_col_name ]:
        try:
            stock_name = yf.Ticker(ticker).info.get("shortName", ticker)
        except Exception:
            stock_name = " "
        stock_names[ ticker ] = stock_name
    print( stock_names )
    d['stock_name'] = d[ticker_col_name].map(stock_names)
    return d

def clean_stock_data( d ):
    d = d.drop(['High', 'Open', 'Low', 'Dividends', 'Stock Splits'], axis=1)
    d = d.dropna(axis=0)
    return d

if __name__ == "__main__":
    print( load_spX00( X00 = 600 ) )
    
    #d = pd.DataFrame( {'val':[10, 7], 'ticker':['NVDA', 'KLAC']} )
    #d = get_stock_names( d, 'ticker' )
