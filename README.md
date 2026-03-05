**S&P500 Strategy Backtesting**

*Project goal*

Leveraging my background in astrophysics, I designed this python code to investigate market dynamics, allowing for the isolation of signal from noise through statistical validation.
This framefork allows the user to investigate the effectiveness of different trading strategies in comparison to a control group (random stocks from the S&P500).
The following strategies can be tested: 
- "Momentum": do stocks that went up recently stay on the same trajectory?
- "Decreasing": do stocks that are below a certain percentage of their past maximum value rebound quickly?
- "Early_recovery": similar to "Decreasing", but the buy signal triggers only after the stock goes up again after a dip
<!-- -->


* Bias mitigation *
- Survivorship Bias Mitigation: Tickers are filtered based on their historical index inclusion dates. The engine only tests stocks that were part of the S&P 500 at the start of the lookback period, preventing the "selection of winners" fallacy.
- Statistical Control Groups: Every strategy run is benchmarked against a randomly sampled control group (Monte Carlo style) to distinguish Alpha (outperformance) from Beta (market returns). It is possible to add a random offset in the buying date of the control stock, to make the moment of buying more random.

* Software Architecture *
The framework is built with a modular, object-oriented approach following the Separation of Concerns principle:
