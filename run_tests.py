"""
Backtests a trading strategy ('momentum', 'declining' or 'early_recovery') on S&P500 stocks,
and compares it with a control group of random S&P500 stocks bought at the same time.
Set the variables below and run:  python3 run_tests.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# in the lines below we import python scripts with functions in the src folder
import src.data_loader as data_loader  
import src.feature_engineer as feature_engineer
import src.analyse_stocks as analyse_stocks
import src.eval_results as eval_results
import src.plotter as plotter
import time
start_time = time.time()
#np.random.seed( 1 )       # for reproducible results when we draw random control stocks

# Define variables that will be used in the object created by the Backtester class
years_back                = 10  # we analyse the data of the last how many years?
track_time                = 365 # in days: for how long do we follow the stock after we 'bought' them?
strategy                  = 'momentum'      # momentum, declining, early_recovery, or all (random) 
n_control                 = 2   # number of stocks we 'buy' at the same time as when the 'buy' signal triggers
control_offset_in_d       = 0     # we can offset the control buying moment
excluded_years            = [] #[2020,2021, 2025, 2026]  # exclude, e.g., years after market crashes. Because those might not be relevant to the current situation.
min_hold_in_d             = 20    # stocks 'bought' less than this many days ago are left out (strategy and control): too little data


# For MOMENTUM strategy:
momentum_factor           = 1.4
momentum_interval_in_days = 40 
# For DECLINING and EARLY_RECOVERY strategy:
frac_remaining            = 0.2
# For EARLY_RECOVERY strategy:
frac_bump                 = 1.2


class BackTester:
    
    """
    This class sets up a workflow for backtesting a trading strategy of choice for stocks in the S&P500.
    It quantitatively tests these strategies and compares them with a control group.
    The settings of the test are passed to __init__ (initialization).
    """

    def __init__( self, strategy, years_back, track_time, momentum_factor=None, momentum_interval_in_days=None,
                  frac_remaining=None, frac_bump=None, n_control=1, control_offset_in_d=0, excluded_years=(), min_hold_in_d=20 ):
        self.strategy                  = strategy
        self.years_back                = years_back
        self.track_time                = track_time
        self.momentum_factor           = momentum_factor
        self.momentum_interval_in_days = momentum_interval_in_days
        self.frac_remaining            = frac_remaining
        self.frac_bump                 = frac_bump
        self.n_control                 = n_control
        self.control_offset_in_d       = control_offset_in_d
        self.excluded_years            = excluded_years
        self.min_hold_in_d             = min_hold_in_d

    def strategy_test_stock( self, stock_ticker, earliest_trigger_date=None ):

        """
        Evaluates the chosen STRATEGY for a specific stock.
        This method will be called by the run_test(...) method below

        Arguments: stock_ticker (for example, 'MSFT' for Microsoft)
                   earliest_trigger_date (optional): buy signals before this date are ignored
        Returns:   - stock data ( i. over whole considered period and ii. between buy and sell signal), 
                   - results of evaluation: stock value ratio at sell/buy moment, holding period, yearly increase
                   - date the buy signal triggered
        """

        d = data_loader.get_stock_data( stock_ticker, self.years_back )        
        if d is None or len(d) <= 2:
           return None, None, None, None, None, None
        d = data_loader.clean_stock_data( d )
        d = feature_engineer.feature_engineer_data( d, self.momentum_interval_in_days )
        d_search = d   # the part of the data where we look for the buy signal
        if pd.notna( earliest_trigger_date ):   # e.g. ignore buy signals from before the stock was added to the S&P500
            d_search = d[ d.Date.dt.tz_localize( None ) > earliest_trigger_date ]
        r = analyse_stocks.get_index_of_buy_moment( d_search, self.strategy, self.momentum_factor, self.momentum_interval_in_days, self.frac_remaining, self.frac_bump )
        if pd.isna( r ): 
           return None, None, None, None, None, None
        dr, strategy_value_ratio, strategy_period, strategy_yrly_incr_in_perc, date0 = analyse_stocks.strategy_value_ratio_and_period_and_yearly_increase( d, r, self.track_time )
        if len(dr) < 2: # we do not want to analyse stocks where the buy signal triggered less than a few days ago - too little data
           return None, None, None, None, None, None
        return d, dr, strategy_value_ratio, strategy_period, strategy_yrly_incr_in_perc, date0 


    def control_test_stock( self, stock_ticker, date0 ):

        """
        Evaluates a number of control stocks bought at or around (if self.control_offset_in_d != 0) the time the strategy buy signal triggers

        Arguments: stock ticker (that we just randomly drew), date where we bought strategy stock
        Returns:   - stock data ( i. over whole considered period and ii. between buy and sell signal), 
                   - results of evaluation: stock value ratio at sell/buy moment, holding period, yearly increase
        """

        c  = data_loader.get_stock_data( stock_ticker, self.years_back )
        if c is None or len(c) <= 1:
           return None, None, None, None, None
        if date0 < c['Date'].iloc[0]:
           return None, None, None, None, None
        cr, control_value_ratio, control_period, control_yrly_incr_in_perc = analyse_stocks.control_value_ratio_and_period_and_yearly_increase( c, self.track_time, date0, self.control_offset_in_d )
        return c, cr, control_value_ratio, control_period, control_yrly_incr_in_perc


    def run_test( self ):

        """
        This method loops over stocks in the S&P500, checks if the buy signal triggers, and if so evaluates the stock and control stock(s).
        """ 

        #         PREPARE for looping over the stocks in the stock_tickers list
        strategy_dates, strategy_cashflows, strategy_value_rats, control_dates, control_cashflows, control_value_rats = [],[],[],[],[],[]
        #stock_tickers = data_loader.load_sp500( self.years_back )
        stock_tickers = data_loader.load_sp500_fromlist( self.years_back )   # load S&P500 at that time from a premade list. Works after 2008
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5))

        #         START the loop
        for stock_ticker in stock_tickers:
            print( f'\n{    stock_ticker}' )
            d, dr, strategy_value_ratio, strategy_period, strategy_yrly_incr_in_perc, date0 = self.strategy_test_stock( stock_ticker )


            #     Evaluate STRATEGY stocks for which the buy signal triggered
            if strategy_value_ratio is not None:
                if date0.year in self.excluded_years: continue
                if strategy_period*365.25 < self.min_hold_in_d: continue
                print( stock_ticker, strategy_value_ratio, strategy_period*365, date0.date())#, strategy_yrly_incr_in_perc )

                plotter.plot_price_vs_time( d, dr, ax1, stock_ticker )
                strategy_value_rats.append( strategy_value_ratio )
                strategy_dates.extend( [dr.Date.iloc[0], dr.Date.iloc[-1]] )
                strategy_cashflows.extend( [ -1,strategy_value_ratio ] )

                # Get value ratio and data for a CONTROL stock for reference.
                for i in range( self.n_control ):
                    control_stock_ticker = np.random.choice( stock_tickers )
                    c, cr, control_value_ratio, control_period, control_yrly_incr_in_perc = self.control_test_stock( control_stock_ticker, date0 )
                    if control_value_ratio is not None and control_period*365.25 >= self.min_hold_in_d:
                        #print( f'{control_stock_ticker} (control)', control_value_ratio, control_period*365, control_yrly_incr_in_perc )
                        plotter.plot_price_vs_time( c, cr, ax2, control_stock_ticker )
                        control_value_rats.append( control_value_ratio )
                        control_dates.extend( [cr.Date.iloc[0], cr.Date.iloc[-1]] )
                        control_cashflows.extend( [ -1,control_value_ratio ] )

        #         EVALUATE the results of strategy and control data
        strategy_avg_yrly_incr_in_perc = eval_results.calc_xirr( strategy_dates, strategy_cashflows, use_utc=True )
        control_avg_yrly_incr_in_perc  = eval_results.calc_xirr( control_dates,  control_cashflows,  use_utc=True )
        print( f'\nAverage yearly increase of STRATEGY (N={len(strategy_dates)/2}): {self.strategy} = {strategy_avg_yrly_incr_in_perc}%' )
        print(   f'Average yearly increase of CONTROL (N={len(control_dates)/2}) stocks = {control_avg_yrly_incr_in_perc}%\n' )
        print( self.momentum_interval_in_days, self.momentum_factor, self.track_time, strategy_avg_yrly_incr_in_perc, control_avg_yrly_incr_in_perc, int(len( strategy_dates)/2+0.5) )
        print( 'KS test:', eval_results.calc_p_value( strategy_value_rats, control_value_rats ) )
        print( f'That took {int(time.time()-start_time+0.5)} s'  )

        # WHEN RUNNING TESTS: keep a local list with results for different momentum_factors etc
        #with open( "notes_and_tests/results_of_runtest_mom_10y_not20.txt", "a" ) as f:
        #    f.write( f"\n{strategy_avg_yrly_incr_in_perc},{self.momentum_factor},{self.momentum_interval_in_days},{self.track_time},{int(len( strategy_dates)/2+0.5)}" ) 
        #    #f.write( f"\n{strategy_avg_yrly_incr_in_perc},{self.frac_remaining},{self.frac_bump},{self.track_time},{int(len( strategy_dates)/2+0.5)}" ) 

        plotter.prettify_and_show( ax1,ax2,self.strategy,strategy_avg_yrly_incr_in_perc,control_avg_yrly_incr_in_perc )

                
if __name__ == '__main__':
    momtest = BackTester( strategy, years_back, track_time, momentum_factor, momentum_interval_in_days, 
                          frac_remaining, frac_bump, n_control, control_offset_in_d, excluded_years, min_hold_in_d )
    momtest.run_test()

"""
# Use this block when DOING TESTS
if __name__ == '__main__':
    for momentum_interval_in_days in [10,13,16,20,25,30,40,50,60,80,100,130]:
        for momentum_factor in [1.25,1.30,1.35,1.40,1.45,1.50,1.55,1.60]:
            momtest = BackTester( strategy, years_back, track_time, momentum_factor=momentum_factor, momentum_interval_in_days=momentum_interval_in_days,
                          frac_remaining=frac_remaining, frac_bump=frac_bump, n_control=n_control, control_offset_in_d=control_offset_in_d, excluded_years=excluded_years, min_hold_in_d=min_hold_in_d )
            momtest.run_test()
"""
