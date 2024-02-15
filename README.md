# IEOR4733
Algorithmic Trading Project Alpaca

## Introduction
  This project aims to build a trading system of stocks on Alpaca. There are two modes of execution: 'trade' and 'backtest'

## Market Data Retrieval and Storage:
  See [data_prep.py](data_prep.py)<br>
  The function takes in Alpaca API, the tickers we would like to trade as an iterable-object, timeframe, start date, end date, and the path where the data is saved. Default path is ./Data/. Through api.get_bars(), we get data for each ticker and save them as csv files in the path that we specified

## Trading Strategy Development:
  The plan is to use all [101 Formulaic Alphas](https://arxiv.org/pdf/1601.00991.pdf) and fit an elastic-net regression. Then use Woodbury matrix inversion lemma for efficient portfolio optimisation. However, due to the time limit of this project, we only used alpha_032 as an indicator to choose the top 30 tickers to hold 1 share respectively.

## Code Explanation:
  [main](main.py): select the pool of the tickers that we would like to trade in, select the mode.<br>
  [data_prep](data_prep.py): retrieve and save the data for either trading or backtesting.<br>
  [strategy](strategy.py): specify the strategy that we are going to use, and return the positions we are going to take.<br>
  [trade](trade.py): trade based on the position given for the day.<br>
  [backtest](backtest.py): backtest the strategy that we are going to use.<br>
  
## Testing and Optimization:
  For lack of time, all alphas with no cross-sectional ranking were tested for robustness and alpha_032 is selected due to its top performance of return. Due to lack of data in some of the tickers that we chose, we only bakctested on the period from 2023-01-01 to 2024-02-01. No major withdrawal was observed for all of our alphas. Comparing with benchmark (buying NASDAQ ETF 'QQQ'), the return is significantly higher.
  
## Automation and Scheduling:
  The trading system would be activated each week day at 9:00am to download the data needed for acquire today's position.<br>
  From 9:30am to 4:00pm, the system executes tradings according to the specified strategy.

## Paper Trading and Monitoring:
  Buy orders and Sell orders are printed if needed.

## Results and Lessons Learned:
  My project so far only calculate the positions based on the data from the previous days. Intradays nuances are neglected due to subscription limit. Also, portfolio optimisation has not been implemented due to time limit.
