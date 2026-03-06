import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# in the lines below we import python scripts with functions in the src folder
import src.data_loader as data_loader  
import src.feature_engineer as feature_engineer
import src.analyse_stocks as analyse_stocks
import src.eval_results as eval_results
import src.plotter as plotter
np.random.seed( 1 )       # for reproducible results when we draw random control stocks

# Define variables that will be used in the object created by the Backtester class
years_back                = 10  # we analyse the data of the last how many years?
track_time                = 365 # in days: for how long do we follow the stock after we 'bought' them?
strategy                  = 'momentum'      # momentum, declining, early_recovery, or all (random) 
sector                    = 'all' #'Information Technology'  # 'all' is also allowed.
n_control                 = 5   # number of stocks we 'buy' at the same time as when the 'buy' signal triggers
control_offset_in_d       = 100     # we offset the control buying moment to reduce bias

# For MOMENTUM strategy:
momentum_factor           = 1.4
momentum_interval_in_days = 40 
# For DECLINING and EARLY_RECOVERY strategy:
frac_remaining            = 0.4
# For EARLY_RECOVERY strategy:
frac_bump                 = 1.1


class BackTester:
    
    """
    This class sets up a workflow for backtesting a trading strategy of choice for stocks in the S&P500.
    It quatitatively tests these strategies and compares with a control group.
    Things that can be are inserted in __init__ (initialization).
    """

    def __init__( self, strategy, sector, years_back, track_time, momentum_factor, momentum_interval_in_days, frac_remaining, frac_bump, n_control, control_offset_in_d ):
        self.strategy                  = strategy
        self.sector                    = sector
        self.years_back                = years_back
        self.track_time                = track_time
        self.momentum_factor           = momentum_factor
        self.momentum_interval_in_days = momentum_interval_in_days
        self.frac_remaining            = frac_remaining
        self.frac_bump                 = frac_bump
        self.n_control                 = n_control
        self.control_offset_in_d       = control_offset_in_d

    def strategy_test_stock( self, stock_ticker ):

        """
        Evaluates the chosen STRATEGY for a specific stock. 
        This method will be called by the run_test(...) method below        
 
        Arguments: stock_ticker (b.v. 'MSFT')
        Returns:   - stock data ( i. over whole considered period and ii. between buy and sell signal), 
                   - results of evaluation: stock value ratio at sell/buy moment, holding period, yearly increase
                   - date the buy signal triggered
        """

        d = data_loader.get_stock_data( stock_ticker, self.years_back )        
        if d is None or len(d) <= 1:
           return None, None, None, None, None, None
        d = data_loader.clean_stock_data( d )
        d = feature_engineer.feature_engineer_data( d, self.momentum_interval_in_days )
        r = analyse_stocks.get_index_of_buy_moment( d, self.strategy, self.momentum_factor, self.momentum_interval_in_days, self.frac_remaining, self.frac_bump )
        if pd.isna( r ): 
           return None, None, None, None, None, None
        dr, strategy_value_ratio, strategy_period, strategy_yrly_incr_in_perc, date0 = analyse_stocks.strategy_value_ratio_and_period_and_yearly_increase( d, r, self.track_time )
        return d, dr, strategy_value_ratio, strategy_period, strategy_yrly_incr_in_perc, date0 


    def control_test_stock( self, stock_ticker, date0 ):

        """
        Evaluates a number of control stocks bought at or around (if self.control_offset_in_d /= 0) the time the strategy buy signal triggers

        Arguments: stock ticker (that we just randomly drew), date where we bought strategy stock
        Returns:   - stock data ( i. over whole considered period and ii. between buy and sell signal), 
                   - results of evaluation: stock value ratio at sell/buy moment, holding period, yearly increase
        """

        c  = data_loader.get_stock_data( stock_ticker, self.years_back )
        if c is None or len(c) <= 1:
           return None, None, None, None, None
        cr, control_value_ratio, control_period, control_yrly_incr_in_perc = analyse_stocks.control_value_ratio_and_period_and_yearly_increase( c, self.track_time, date0, self.control_offset_in_d )
        return c, cr, control_value_ratio, control_period, control_yrly_incr_in_perc


    def run_test( self ):

        """
        This method loops over stocks in the S&P500, checks if the buy signal triggers, and if so evaluates the stock and control stock(s).
        """ 

        #         PREPARE for looping over the stocks in the stock_tickers list
        strategy_periods, strategy_value_rats, control_periods, control_value_rats = [],[],[],[]
        stock_tickers = data_loader.load_sp500( self.sector, self.years_back )
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5))

        #         START the loop
        for stock_ticker in stock_tickers:
            print( f'\n{stock_ticker}' )
            d, dr, strategy_value_ratio, strategy_period, strategy_yrly_incr_in_perc, date0 = self.strategy_test_stock( stock_ticker )

            #     Evaluate STRATEGY stocks
            if strategy_value_ratio is not None:
                print( strategy_value_ratio, strategy_period*365, date0.date(), strategy_yrly_incr_in_perc )
                plotter.plot_price_vs_time( d, dr, ax1, stock_ticker )
                strategy_periods.append( strategy_period )
                strategy_value_rats.append( strategy_value_ratio )

                # Get value ratio and data for a CONTROL stock for reference.
                for i in range( n_control ):
                    control_stock_ticker = np.random.choice( stock_tickers )
                    c, cr, control_value_ratio, control_period, control_yrly_incr_in_perc = self.control_test_stock( control_stock_ticker, date0 )
                    if control_value_ratio is not None:
                        print( f'{control_stock_ticker} (control)', control_value_ratio, control_period*365, control_yrly_incr_in_perc )
                        plotter.plot_price_vs_time( c, cr, ax2, stock_ticker )
                        control_periods.append( control_period )
                        control_value_rats.append( control_value_ratio )

        #         EVALUATE the results of strategy and control data
        strategy_avg_yrly_incr_in_perc, strategy_avg_incr_in_perc = eval_results.calc_avg_yrly_incr( strategy_periods, strategy_value_rats )
        control_avg_yrly_incr_in_perc,  control_avg_incr_in_perc  = eval_results.calc_avg_yrly_incr( control_periods,  control_value_rats  )
        print( f'\nAverage yearly increase of STRATEGY (N={len(strategy_periods)}): {self.strategy} = {strategy_avg_yrly_incr_in_perc}%' )
        print(   f'Average yearly increase of CONTROL (N={len(control_periods)}) stocks = {control_avg_yrly_incr_in_perc}%\n' )
        print(   f'Average total increase: {strategy_avg_incr_in_perc}% (STRATEGY) and {control_avg_incr_in_perc} (CONTROL)\n' )
        print( f'These were the variables that we used:\n{vars(self)}\n' )
        print( strategy_value_rats )
        print( control_value_rats )
        print( 'KS test:', eval_results.calc_p_value( strategy_value_rats, control_value_rats ) )
        plotter.prettify_and_show( ax1,ax2,self.strategy,strategy_avg_yrly_incr_in_perc,control_avg_yrly_incr_in_perc )
                

# WAAROM KLEIN VERSCHIL TUSSEN STRAT 1YR AVG_YRLY en TOTAL_INCR?
            
if __name__ == '__main__':
    momtest = BackTester( strategy, sector, years_back, track_time, momentum_factor, momentum_interval_in_days, 
                          frac_remaining, frac_bump, n_control, control_offset_in_d )
    momtest.run_test()

"""
if __name__ == '__main__':
    for momentum_factor in [1.4, 1.5]:
        for momentum_interval_in_days in [50, 100]:
            momtest = BackTester( strategy, sector, years_back, track_time, momentum_factor, momentum_interval_in_days,
                          frac_remaining, frac_bump, n_control, control_offset_in_d )
            momtest.run_test() 
# https://github.com/bkestelman/sp500_historical_components?tab=readme-ov-file # for removed tickers
"""
