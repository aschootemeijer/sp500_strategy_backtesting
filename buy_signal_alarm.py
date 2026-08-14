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

overwrite_readme          = True
append_to_results         = True
momentum_factor           = 1.4
track_time                = 183  # in days
momentum_interval_in_days = 40
X00                       = 500

class BuySignalGenerator( BackTester ):

    """
    This class inherits all methods from the BackTester class in the script run_tests.py.
    We add an extra method that gives names and dates for stocks in the S&P500 for which the buy signal recently triggered.
    We use this and store these data in the README.md file (if overwrite_readme is True) 
    """

    def run_buy_signal_alarm( self ):

        # SET UP a few things before we start evaluating the stocks
        strategy_dates, strategy_cashflows, strategy_value_rats, control_dates, control_cashflows, control_value_rats = [],[],[],[],[],[]
        #stock_tickers = data_loader.load_sp500( self.sector, self.years_back )
        stock_tickers = data_loader.load_spX00( X00=X00 )
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5))
        b = pd.DataFrame( columns = ['trigger_date','stock_ticker'] )

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
                b.at[ ind, 'value_ratio' ]  = strategy_value_ratio 
        b = b.sort_values( by='trigger_date', ascending=False ).reset_index( drop=True )

        # MODIFY DATAFRAME to add column with full name
        b  = data_loader.get_stock_names( b, 'stock_ticker' )      # adds column: stock_ticker
        b  = feature_engineer.add_perc_column( b, 'value_ratio' )  # adds column: perc_since_trigger
        bw = b[[ 'trigger_date','stock_ticker','stock_name','perc_since_trigger']]
        
        # WRITE TO FILE
        datetime_write = datetime.datetime.now().strftime( "%Y-%m-%d %H:%M" )
        df_write       = bw.head(25).to_html( index=False )
        datafile2write = ( f"Last automatic update: {datetime_write}<br>\n"
                           f"Buy signal trigger: at least {int(100*(self.momentum_factor-1)+0.5)}% increase in two successive {self.momentum_interval_in_days} day periods<br>\n"
                           #f"Average increase since trigger: {np.round( np.average(100*(b.value_ratio-1)),1)}%<br>"
                           f"{df_write}" )
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
        print( '\n\n',bw)
        strategy_avg_yrly_incr_in_perc = eval_results.calc_xirr( strategy_dates, strategy_cashflows )
        control_avg_yrly_incr_in_perc  = None
        plotter.prettify_and_show( ax1,ax2,self.strategy,strategy_avg_yrly_incr_in_perc,control_avg_yrly_incr_in_perc )

        # keep a local list with results for different momentum_factors etc
        with open( "results_of_buysig.txt", "a" ) as f:
           f.write( f"{strategy_avg_yrly_incr_in_perc},{momentum_factor},{momentum_interval_in_days},{track_time},{len(bw)},{X00}" ) 

if __name__ == '__main__':
    n_control = 0
    _strategy        = 'momentum'
    _sector          = 'all'
    _years_back      = 1
    _frac_remaining, _frac_bump, _control_offset_in_d = 0.5, 0.2, 0  # we don't use these variables because we 
    buy_signal_alarm_obj = BuySignalGenerator( _strategy, _sector, _years_back, track_time, momentum_factor, momentum_interval_in_days, 
                           _frac_remaining, _frac_bump, n_control, _control_offset_in_d  )
    buy_signal_alarm_obj.run_buy_signal_alarm()

