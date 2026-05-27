import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

# import local classes and functions
from run_tests import BackTester
import src.data_loader as data_loader  
import src.feature_engineer as feature_engineer
import src.analyse_stocks as analyse_stocks
import src.eval_results as eval_results
import src.plotter as plotter

overwrite_readme = True


class BuySignalGenerator( BackTester ):

    """
    This class inherits all methods from the BackTester class in the script run_tests.py.
    We add an extra method that gives names and dates for stocks in the S&P500 for which the buy signal recently triggered.
    We use this and store these data in the README.md file (if overwrite_readme is True) 
    """

    def run_buy_signal_alarm( self ):

        # SET UP a few things before we start evaluating the stocks
        strategy_dates, strategy_cashflows, strategy_value_rats, control_dates, control_cashflows, control_value_rats = [],[],[],[],[],[]
        stock_tickers = data_loader.load_sp500( self.sector, self.years_back )
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5))
        b = pd.DataFrame( columns = ['stock_ticker','trigger_date'] )

        # EVALUATE stocks; CREATE DATAFRAME of recent buy signal triggers
        for stock_ticker in stock_tickers:
            print( f'\n{stock_ticker}' )
            d, dr, strategy_value_ratio, strategy_period, strategy_yrly_incr_in_perc, date0 = self.strategy_test_stock( stock_ticker )

            # Proceed only with stocks for which the buy signal triggered
            if strategy_value_ratio is not None:
                print( strategy_value_ratio, strategy_period*365, date0.date(), strategy_yrly_incr_in_perc )
                plotter.plot_price_vs_time( d, dr, ax1, stock_ticker )
                strategy_value_rats.append( strategy_value_ratio )
                strategy_dates.extend( [dr.Date.iloc[0], dr.Date.iloc[-1]] )
                strategy_cashflows.extend( [ -1,strategy_value_ratio ] )
                ind = len( b )
                b.at[ ind, 'stock_ticker' ] = stock_ticker
                b.at[ ind, 'trigger_date' ] = date0.date()
        b = b.sort_values( by='trigger_date', ascending=False ).reset_index( drop=True )
        
        # WRITE TO FILE
        datetime_write = datetime.datetime.now().strftime( "%Y-%m-%d %H:%M" )
        df_write       = b.head(15).to_html( index=False )
        datafile2write = ( f"Last automatic update: {datetime_write}<br>\n"
                           f"Momentum_factor: {self.momentum_factor}; momentum_interval: {self.momentum_interval_in_days} days<br>\n"
                           f"Most recently triggered buy signals:\n"
                           f"{df_write}" )
        # keep a local list ..
        with open( "auto_upd_buys.txt", "w" ) as f:
            print( datafile2write, file=f )
        # .. and insert latest data in README.md
        if overwrite_readme is True:
            # update the readme file that will be upoaded to github
            with open( "README.md", "r" ) as fr:
                readme_content = fr.read()
            data_start_tag = "<!-- DATA_START -->"
            data_end_tag   = "<!-- DATA_END -->"
            top_txt        = readme_content.split( data_start_tag )[0]
            bottom_txt     = readme_content.split( data_end_tag )[1]
            updated_readme_content = f"{top_txt}{data_start_tag}\n{datafile2write}\n{data_end_tag}{bottom_txt}"
            with open( "README.md", "w" ) as fw:
                fw.write( updated_readme_content )

        # DISPLAY whole list of stocks; including a graph and calculation of their performace
        pd.set_option('display.max_rows', None)
        print( '\n\n',b)
        strategy_avg_yrly_incr_in_perc = eval_results.calc_xirr( strategy_dates, strategy_cashflows )
        control_avg_yrly_incr_in_perc  = None
        plotter.prettify_and_show( ax1,ax2,self.strategy,strategy_avg_yrly_incr_in_perc,control_avg_yrly_incr_in_perc )
            

if __name__ == '__main__':
    strategy        = 'momentum'
    sector          = 'all'
    momentum_factor = 1.4
    years_back      = 2 
    track_time      = 183  # in days
    momentum_interval_in_days = 40
    n_control = 0
    _frac_remaining, _frac_bump, _control_offset_in_d = 0.5, 0.2, 0  # we don't use these variables because we 
    buy_signal_alarm_obj = BuySignalGenerator( strategy, sector, years_back, track_time, momentum_factor, momentum_interval_in_days, 
                           _frac_remaining, _frac_bump, n_control, _control_offset_in_d  )
    buy_signal_alarm_obj.run_buy_signal_alarm()

