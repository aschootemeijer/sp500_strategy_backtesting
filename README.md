## S&P500 Strategy Backtesting
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white) ![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black) ![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white) ![Yahoo!](https://img.shields.io/badge/Yahoo!-6001D2?style=for-the-badge&logo=Yahoo!&logoColor=white) ![SciPy](https://img.shields.io/badge/SciPy-%230C55A5.svg?style=for-the-badge&logo=scipy&logoColor=%white)

### Project goal
Leveraging my background in astrophysics, I designed this python code to investigate market dynamics of the S&P500. The code can isolate signal from noise through statistical validation.
This is an object-oriented programming (OOP)-based framework that allows the user to investigate the effectiveness of different trading strategies in comparison to a control group (random stocks from the S&P500).
The following strategies can be tested: 
- "Momentum": do stocks that went up recently stay on the same trajectory?
- "Decreasing": do stocks that are below a certain percentage of their past maximum value rebound quickly?
- "Early_recovery": similar to "Decreasing", but the buy signal triggers only after the stock goes up again after a dip

### Result highlight 1: strategy test 
<b>Method:</b> Investigated the "Momentum" strategy for a buy signal that triggers if an S&P500 stock has increased by at least 40% for two successive 40 day periods. The stocks are sold a year after the buy signal triggers. For each stock, up to five control stocks were bought with a random offset of +/- 100 days.<br>
<b>Result:</b> 54.9% yearly increase for the 24 "Momentum" strategy stocks, and 27.3% yearly increase for the 99 control stocks. The control stocks increased more than the typical S&P500 value of ~11% because they were bought at relatively favorable times. A Kolgomorov-Smirnov test yielded a p=99.7% chance that the "Momentum" and control groups were drawn from different probability distributions. Therefore, the good performance of the "Momentum" stocks is statistically significant.

<img width="550" height="250" alt="mom_40d_f1p4_dcon100d" src="https://github.com/user-attachments/assets/23071ef3-2d5a-4a4c-9c2d-e1048c9d5339" />

### Result highlight 2: buying recommendations
For the strategy tested in Result highlight (1), we obtain the stocks for which a buy signal triggered in data of the last 1 year. The positives easily outweigh the negatives.<br> 
<b>Guidelines for investors:</b> i) after the buy signal triggers, buy within 1-2 months; ii) around 1 year after the buy signal triggers, these stocks are meant to be sold, as they are expected to become less profitable.

<!-- DATA_START -->
Last automatic update: 2026-08-19 10:03<br>
Buy signal trigger: at least 40% increase in two successive 40 day periods<br>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>trigger_date</th>
      <th>stock_ticker</th>
      <th>stock_name</th>
      <th>perc_since_trigger</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>2026-07-09</td>
      <td>FTNT</td>
      <td>Fortinet, Inc.</td>
      <td>🔴 -3.5%</td>
    </tr>
    <tr>
      <td>2026-06-30</td>
      <td>KLAC</td>
      <td>KLA Corporation</td>
      <td>🔴 -35.4%</td>
    </tr>
    <tr>
      <td>2026-06-30</td>
      <td>LRCX</td>
      <td>Lam Research Corporation</td>
      <td>🔴 -24.3%</td>
    </tr>
    <tr>
      <td>2026-06-30</td>
      <td>AMAT</td>
      <td>Applied Materials, Inc.</td>
      <td>🔴 -28.9%</td>
    </tr>
    <tr>
      <td>2026-06-18</td>
      <td>PANW</td>
      <td>Palo Alto Networks, Inc.</td>
      <td>🟢 30.0%</td>
    </tr>
    <tr>
      <td>2026-06-08</td>
      <td>HUM</td>
      <td>Humana Inc.</td>
      <td>🟢 7.6%</td>
    </tr>
    <tr>
      <td>2026-06-02</td>
      <td>CRWD</td>
      <td>CrowdStrike Holdings, Inc.</td>
      <td>🟢 10.8%</td>
    </tr>
    <tr>
      <td>2026-05-29</td>
      <td>HPE</td>
      <td>Hewlett Packard Enterprise Comp</td>
      <td>🟢 29.8%</td>
    </tr>
    <tr>
      <td>2026-05-29</td>
      <td>DDOG</td>
      <td>Datadog, Inc.</td>
      <td>🔴 -0.5%</td>
    </tr>
    <tr>
      <td>2026-05-14</td>
      <td>ON</td>
      <td>ON Semiconductor Corporation</td>
      <td>🔴 -32.9%</td>
    </tr>
    <tr>
      <td>2026-05-11</td>
      <td>VRT</td>
      <td>Vertiv Holdings, LLC</td>
      <td>🔴 -25.9%</td>
    </tr>
    <tr>
      <td>2026-05-08</td>
      <td>GLW</td>
      <td>Corning Incorporated</td>
      <td>🔴 -14.3%</td>
    </tr>
    <tr>
      <td>2026-05-06</td>
      <td>DELL</td>
      <td>Dell Technologies Inc.</td>
      <td>🟢 96.6%</td>
    </tr>
    <tr>
      <td>2026-05-06</td>
      <td>FLEX</td>
      <td>Flex Ltd.</td>
      <td>🔴 -10.8%</td>
    </tr>
    <tr>
      <td>2026-05-06</td>
      <td>AMD</td>
      <td>Advanced Micro Devices, Inc.</td>
      <td>🟢 15.0%</td>
    </tr>
    <tr>
      <td>2026-05-05</td>
      <td>FIX</td>
      <td>Comfort Systems USA, Inc.</td>
      <td>🔴 -11.5%</td>
    </tr>
    <tr>
      <td>2026-05-05</td>
      <td>MRVL</td>
      <td>Marvell Technology, Inc.</td>
      <td>🟢 28.0%</td>
    </tr>
    <tr>
      <td>2026-04-24</td>
      <td>INTC</td>
      <td>Intel Corporation</td>
      <td>🟢 17.1%</td>
    </tr>
    <tr>
      <td>2026-02-06</td>
      <td>TER</td>
      <td>Teradyne, Inc.</td>
      <td>🟢 26.5%</td>
    </tr>
    <tr>
      <td>2026-02-03</td>
      <td>STX</td>
      <td>Seagate Technology Holdings PLC</td>
      <td>🟢 88.9%</td>
    </tr>
    <tr>
      <td>2026-01-21</td>
      <td>MRNA</td>
      <td>Moderna, Inc.</td>
      <td>🟢 14.5%</td>
    </tr>
    <tr>
      <td>2026-01-02</td>
      <td>ALB</td>
      <td>Albemarle Corporation</td>
      <td>🔴 -5.3%</td>
    </tr>
    <tr>
      <td>2026-01-02</td>
      <td>MU</td>
      <td>Micron Technology, Inc.</td>
      <td>🟢 209.4%</td>
    </tr>
    <tr>
      <td>2025-12-12</td>
      <td>ECHO</td>
      <td>EchoStar Corporation</td>
      <td>🟢 6.2%</td>
    </tr>
    <tr>
      <td>2025-12-11</td>
      <td>LITE</td>
      <td>Lumentum Holdings Inc.</td>
      <td>🟢 147.7%</td>
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

<!-- 
### Getting started
- Clone the repository.
- Install dependencies: pip install pandas numpy yfinance matplotlib
- Run the backtest with: python3 run_tests.py
-->

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
