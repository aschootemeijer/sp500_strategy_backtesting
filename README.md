## S&P500 Strategy Backtesting
![Python Version](https://img.shields.io)
![Pandas](https://img.shields.io)
![NumPy](https://img.shields.io)
![Matplotlib](https://img.shields.io)
![Requests](https://img.shields.io)

### Project goal
Leveraging my background in astrophysics, I designed this python code to investigate market dynamics of the S&P500. The code for the isolation of signal from noise through statistical validation.
This is a framework that allows the user to investigate the effectiveness of different trading strategies in comparison to a control group (random stocks from the S&P500).
The following strategies can be tested: 
- "Momentum": do stocks that went up recently stay on the same trajectory?
- "Decreasing": do stocks that are below a certain percentage of their past maximum value rebound quickly?
- "Early_recovery": similar to "Decreasing", but the buy signal triggers only after the stock goes up again after a dip

### Bias mitigation
- Survivorship Bias Mitigation: Stock tickers are filtered based on their historical index inclusion dates. The engine only tests stocks that were part of the S&P 500 at the start of the lookback period, preventing the "selection of winners" fallacy.
- Statistical Control Groups: Every strategy run is benchmarked against a randomly sampled control group (Monte Carlo style) to distinguish Alpha (outperformance) from Beta (market returns). It is possible to add a random offset in the buying date of the control stock, to make the moment of buying more random.

### Software Architecture
The framework is built with a modular, object-oriented programming (OOP) approach following the Separation of Concerns principle:
- data_loader.py: The current S&P 500 stocks are obtained from Wikipedia using web scraping. Their data is then automatically ingested via Yahoo Finance.
- feature_engineer.py: Transformation of raw time-series data into technical indicators and signals.
- analyse_stocks.py: The buying signal generation engine and performance calculator for individual stocks
- eval_results.py: evaluates the performance of an enseble of stocks (strategy or control)
- plotter.py: Visualization engine for side-by-side comparison of strategy vs. control equity curves.

### Result highlight
For the "Momentum" strategy and a buy signal that triggers if a stock has increased by 70% for two successive 200 day periods, the "Momentum" strategy outperformed the S&P500 by a factor 1.5.

### Future work
Thanks to the OOP design of the code, it is straightforward to extend it to systematically explore the variables used for buy signal generation (e.g., for the "Momentum" strategy, these variables are how much the stock price increases and in which time period). This allows for the optimization of these strategies. <!-- One can simply change:
if __name__ == '__main__':
    momtest = BackTester( strategy, sector, years_back, track_time, momentum_factor, momentum_interval_in_days,
                          frac_remaining, frac_bump, n_control, control_offset_in_d )
    momtest.run_test()
into:
if __name__ == '__main__':
    for momentum_factor in [1.3, 1.35, 1.4, 1.45, 1.5]:
        for momentum_interval_in_days in [30, 60, 90, 120]:
            momtest = BackTester( strategy, sector, years_back, track_time, momentum_factor, momentum_interval_in_days,
                          frac_remaining, frac_bump, n_control, control_offset_in_d )
            momtest.run_test()
            -->

### Getting started
- Clone the repository.
- Install dependencies: pip install pandas numpy yfinance matplotlib
- Run the backtest with: python3 run_tests.py
