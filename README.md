## S&P500 Strategy Backtesting
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white) ![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black) ![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white) ![Yahoo!](https://img.shields.io/badge/Yahoo!-6001D2?style=for-the-badge&logo=Yahoo!&logoColor=white) ![SciPy](https://img.shields.io/badge/SciPy-%230C55A5.svg?style=for-the-badge&logo=scipy&logoColor=%white)

### Getting started
- Clone the repository.
- Install dependencies: pip install pandas numpy yfinance matplotlib
- Run the backtest with: python3 run_tests.py

### Project goal
Leveraging my background in astrophysics, I designed this python code to investigate market dynamics of the S&P500. The code can isolate signal from noise through statistical validation.
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
- eval_results.py: evaluates the performance of an ensemble of stocks (strategy or control)
- plotter.py: Visualization engine for side-by-side comparison of strategy vs. control equity curves.

### Result highlight
Investigated the "Momentum" strategy for a buy signal that triggers if an S&P500 stock has increased by at least 40% for two successive 40 day periods. The stocks are sold a year after the buy signal triggers. For each stock, up to five control stocks were bought with a random offset of +/- 100 days. Result: 62.1% yearly increase for the 33 "Momentum" strategy stocks, and 23.6% yearly increase for the 139 control stocks. The control stocks increased more than the typical S&P500 value of ~11% because they were bought at relatively favorable times. The "Momentum" stocks outperformed the control stocks by rather large margin. A Kolgomorov-Smirnov test yielded a 98.0% chance that the "Momentum" and coltrol groups were drawn from different probability distributions. Therefore, the good performance of the "Momentum" stocks is statistically significant. 
<img width="550" height="250" alt="mom_40d_f1p4_dcon100d" src="https://github.com/user-attachments/assets/5adb90cd-0812-4e88-ad70-e09e70bdda4a" />


### Future work
- The result presented above contains many stocks for which the buy signal triggered in the post-covid-plunge (stock) recovery period. Would the result hold if the year 2020 is excluded from the analysis?
- Some stocks have been taken out of the S&P500 over time. One can include these by using the log of changes to the Wikipedia S&P500 website. I expect especially the analysis of "Declining" and "Early_recovery" strategy stocks to benefit from this.
- Thanks to the OOP design of the code, it is straightforward to extend it to systematically explore the variables used for buy signal generation (e.g., for the "Momentum" strategy, these variables are how much the stock price increases and in which time period). All that is needed for this is adding one line with a for loop after the "if __name__ is '__main__':" line (per explored variable). This allows for the optimization of these strategies.

<!-- One can simply change:
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
