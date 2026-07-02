## S&P500 Strategy Backtesting
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white) ![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black) ![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white) ![Yahoo!](https://img.shields.io/badge/Yahoo!-6001D2?style=for-the-badge&logo=Yahoo!&logoColor=white) ![SciPy](https://img.shields.io/badge/SciPy-%230C55A5.svg?style=for-the-badge&logo=scipy&logoColor=%white)

### Project goal
Leveraging my background in astrophysics, I designed this python code to investigate market dynamics of the S&P500. The code can isolate signal from noise through statistical validation.
This is an object-oriented programming (OOP)-based framework that allows the user to investigate the effectiveness of different trading strategies in comparison to a control group (random stocks from the S&P500).
The following strategies can be tested: 
- "Momentum": do stocks that went up recently stay on the same trajectory?
- "Decreasing": do stocks that are below a certain percentage of their past maximum value rebound quickly?
- "Early_recovery": similar to "Decreasing", but the buy signal triggers only after the stock goes up again after a dip

### Result highlight (1)
<b>Method:</b> Investigated the "Momentum" strategy for a buy signal that triggers if an S&P500 stock has increased by at least 40% for two successive 40 day periods. The stocks are sold a year after the buy signal triggers. For each stock, up to five control stocks were bought with a random offset of +/- 100 days.<br>
<b>Result:</b> 54.9% yearly increase for the 24 "Momentum" strategy stocks, and 27.3% yearly increase for the 99 control stocks. The control stocks increased more than the typical S&P500 value of ~11% because they were bought at relatively favorable times. A Kolgomorov-Smirnov test yielded a p=99.7% chance that the "Momentum" and control groups were drawn from different probability distributions. Therefore, the good performance of the "Momentum" stocks is statistically significant.

<img width="550" height="250" alt="mom_40d_f1p4_dcon100d" src="https://github.com/user-attachments/assets/23071ef3-2d5a-4a4c-9c2d-e1048c9d5339" />

### Result highlight (2)
For the strategy tested in Result highlight (1), we obtain the stocks with the most recently triggered buy signals. 
<!-- DATA_START -->
Last automatic update: 2026-07-02 10:02<br>
Momentum_factor: 1.4; momentum_interval: 40 days<br>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>stock_ticker</th>
      <th>trigger_date</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>KLAC</td>
      <td>2026-06-30</td>
    </tr>
    <tr>
      <td>LRCX</td>
      <td>2026-06-30</td>
    </tr>
    <tr>
      <td>AMAT</td>
      <td>2026-06-30</td>
    </tr>
    <tr>
      <td>PANW</td>
      <td>2026-06-18</td>
    </tr>
    <tr>
      <td>HUM</td>
      <td>2026-06-08</td>
    </tr>
    <tr>
      <td>CRWD</td>
      <td>2026-06-02</td>
    </tr>
    <tr>
      <td>DDOG</td>
      <td>2026-05-29</td>
    </tr>
    <tr>
      <td>HPE</td>
      <td>2026-05-29</td>
    </tr>
    <tr>
      <td>ON</td>
      <td>2026-05-14</td>
    </tr>
    <tr>
      <td>GLW</td>
      <td>2026-05-08</td>
    </tr>
    <tr>
      <td>AMD</td>
      <td>2026-05-06</td>
    </tr>
    <tr>
      <td>DELL</td>
      <td>2026-05-06</td>
    </tr>
    <tr>
      <td>FIX</td>
      <td>2026-05-05</td>
    </tr>
    <tr>
      <td>INTC</td>
      <td>2026-04-24</td>
    </tr>
    <tr>
      <td>STX</td>
      <td>2026-02-03</td>
    </tr>
  </tbody>
</table>
<!-- DATA_END -->

### Software Architecture
The framework is built with a modular, OOP approach following the Separation of Concerns principle:
- src/data_loader.py: Loads the stocks that were in the S&P500 at the start of the lookback period. Loads time-series data for these stocks.
- src/feature_engineer.py: Transformation of raw time-series data into technical indicators and signals.
- src/analyse_stocks.py: The buying signal generation engine and performance calculator for individual stocks.
- src/eval_results.py: Evaluates the performance of an ensemble of stocks (strategy or control).
- src/plotter.py: Visualization engine for side-by-side comparison of strategy vs. control equity curves.
- run_tests.py: Puts the modules above to use by testing a strategy. Example: Result highlight (1).
- buy_signal_generator.py: Creates a table of stocks for which a buy signal triggered recently. This is shown under Result highlight (2).<br>The table is updated daily. This is fully automated with Cron.

### Bias mitigation
<!-- - Survivorship Bias Mitigation: Stock tickers are filtered based on their historical index inclusion dates. The engine only tests stocks that were part of the S&P 500 at the start of the lookback period, preventing the "selection of winners" fallacy. -->
- Survivorship Bias Mitigation: Stock tickers are selected that were part of the S&P 500 at the start of the lookback period (using a local file with historical S&P 500 constituents). This prevents the infamous "selection of winners" fallacy. 
- Statistical Control Groups: Every strategy run is benchmarked against a randomly sampled control group (Monte Carlo style) to distinguish Alpha (outperformance) from Beta (market returns). It is possible to add a random offset in the buying date of the control stock, to make the moment of buying more random.

### Future work
<!-- - The result presented above contains many stocks for which the buy signal triggered in the post-covid-plunge (stock) recovery period. Would the result hold if the year 2020 is excluded from the analysis?
- Some stocks have been taken out of the S&P500 over time. One can include these by using the log of changes to the Wikipedia S&P500 website. I expect especially the analysis of "Declining" and "Early_recovery" strategy stocks to benefit from this. -->
- Thanks to the OOP design of the code, it is straightforward to extend it to systematically explore the variables used for buy signal generation (e.g., for the "Momentum" strategy, these variables are how much the stock price increases and in which time period). All that is needed for this is adding one line with a for loop after the "if __name__ is '__main__':" line (per explored variable). This allows for the optimization of these strategies.

### Getting started
- Clone the repository.
- Install dependencies: pip install pandas numpy yfinance matplotlib
- Run the backtest with: python3 run_tests.py

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
