import yfinance as yf
import pandas as pd
import requests
from io import StringIO
import datetime

def load_sp500( sector, years_back ):
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    headers = {"User-Agent": "Mozilla/5.0"}    # else we get access denied
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    sp500 = pd.read_html( StringIO( r.text ) )[0]
    if not sector == 'all':
        sp500 = sp500[ sp500['GICS Sector'] == sector ]
    #print( sp500.columns )
    #print( sp500[['Symbol','Security','GICS Sub-Industry']] )
    # these two lines below are to prevent bias: remove succesfull stocks that were added after years_back
    sp500['Date added'] = pd.to_datetime( sp500['Date added'] )
    sp500 = sp500[ sp500["Date added"].dt.year <= datetime.datetime.now().year - years_back ]
    stock_ticker_list = sp500['Symbol'].tolist()
    return stock_ticker_list


def get_stock_data( stock_ticker, years_back ):
    d_all = yf.Ticker( stock_ticker )
    d     = d_all.history( period=f'{years_back}y', auto_adjust=True )
    d     = d.reset_index()
    if len(d) <= 1: 
        return
    else:
        return d

def clean_stock_data( d ):
    d = d.drop(['High', 'Open', 'Low', 'Dividends', 'Stock Splits'], axis=1)
    d = d.dropna(axis=0)
    return d


