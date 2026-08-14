import yfinance as yf
import pandas as pd
import requests
from io import StringIO
import datetime

def load_sp500_fromlist( _sector, years_back ):
    sp500_all = pd.read_csv( '/mnt/c/Users/hp/Desktop/dinges/fin/experimenteren/tickerlists/sp500_monthly.csv', parse_dates=['date'] )
    then  = datetime.datetime.now() - pd.offsets.DateOffset( years=10 )
    sp500 = sp500_all[ (sp500_all.date.dt.year == then.year) & (sp500_all.date.dt.month == then.month) ] 
    return sp500.iloc[0,1:].dropna().tolist()
    
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

def load_spX00( X00 = 500 ): # 400, 500, or 600
    url = f"https://en.wikipedia.org/wiki/List_of_S%26P_{X00}_companies"
    print( url )
    headers = {"User-Agent": "Mozilla/5.0"}    # else we get access denied
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    spX00 = pd.read_html( StringIO( r.text ) )[0]
    stock_ticker_list = spX00['Symbol'].tolist()
    return stock_ticker_list 


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
