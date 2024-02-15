import alpaca_trade_api as tradeapi
import pandas as pd
import trade
import backtest

api_key = 'PKCUBKM203V71FIK9DBN'
api_secret = 'ZvGyXvpSPEbgBFP4MzdaIEhXlBMSQpCd0ZWAZReK'
base_url = 'https://paper-api.alpaca.markets'

def main(mode):
    # Initialise Alpaca API
    api = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')

    # Prepare the pool of tickers that we would like to choose from
    nasdaq_list = pd.read_csv('./NASDAQ_constituents.csv')
    symbols = nasdaq_list['Symbol'].values

    # In trading mode if 'trade' else in backtesting mode
    if mode == 'trade':
        trade.trade(symbols, api)
    else:
        backtest.backtest(symbols, api)

if __name__ == '__main__':
    main('backtest')
