import pandas as pd
import alpaca_trade_api as tradeapi
import time
import datetime
from datetime import date, timedelta
import data_prep
import strategy

def get_current_portfolio(api):
    """
    Get current portfolio
    param: api
    return: a dict of current portfolio whose keys are symbols
        and values are a dict of quantity qty,
            current price current_price, market value market_value
    """
    positions = api.list_positions()
    portfolio = {}
    for position in positions:
        symbol = position.symbol
        qty = int(position.qty)
        current_price = float(position.current_price)
        market_value = float(position.market_value)
        portfolio[symbol] = {
            'qty': qty,
            'current_price': current_price,
            'market_value': market_value
        }
    return portfolio

def is_weekday():
    # Get the current day of the week as an integer (Monday is 0, Sunday is 6)
    today = datetime.datetime.today().weekday()
    # Check if today is a weekday (Monday through Friday)
    return 0 <= today <= 4

def is_close_to_trading_hours():
    # Get the current time
    now = datetime.datetime.now()
    # Define trading hours in 24-hour format
    start_time = datetime.time(9, 00)
    end_time = datetime.time(9, 30)
    # Check if the current time is within trading hours
    return start_time <= now.time() <= end_time

def is_within_trading_hours():
    # Get the current time
    now = datetime.datetime.now()
    # Define trading hours in 24-hour format
    start_time = datetime.time(9, 30)
    end_time = datetime.time(16, 0)
    # Check if the current time is within trading hours
    return start_time <= now.time() <= end_time

def trade(symbols, api):
    while True:
        # buy/sell attempt in every 5 seconds
        try:
            if is_weekday():
                if is_close_to_trading_hours():
                    # get the data from yesterday to 460 days prior
                    timeframe = tradeapi.TimeFrame.Day
                    end_date = date.today() - timedelta(days=1)
                    start_date = end_date - timedelta(days=230 * 2)
                    data_prep.data_download(api, symbols, timeframe, start_date.isoformat(), end_date.isoformat())

                    # get today's position from yesterday's data
                    positions = strategy.get_positions(symbols).iloc[-1, :]
                elif is_within_trading_hours():
                    curr_portfolio = get_current_portfolio(api)
                    for symbol in symbols:
                        historical_data = api.get_bars(symbol, '1Min', limit=1).df
                        last_close_price = historical_data['close'].iloc[-1]

                        # if we have this ticker and today's position should be 0, sell
                        # if we don't have this ticker and today's position is non-zero, buy
                        if positions[symbol+'_alpha032'] == 0:
                            if symbol in curr_portfolio.keys():
                                api.submit_order(
                                    symbol=symbol,
                                    qty=str(positions[symbol+'_alpha032']),
                                    side='sell',
                                    type='limit',
                                    time_in_force='gtc',
                                    limit_price=round(last_close_price * 0.9, 2),  # Place a limit order slightly below the current price
                                )
                                print(f"Sell {symbol} placed at {last_close_price}")
                        else:
                            if symbol not in curr_portfolio.keys():
                                api.submit_order(
                                    symbol=symbol,
                                    qty=str(positions[symbol+'_alpha032']),
                                    side='buy',
                                    type='limit',
                                    time_in_force='gtc',
                                    limit_price=round(last_close_price * 1.1, 2),  # Place a limit order slightly above the current price
                                )
                                print(f"Buy {symbol} placed at {last_close_price}")
                    time.sleep(2)
                else:
                    time.sleep(61200)
            else:
                time.sleep(86400)

        except Exception as e:
            print(f"An error occurred: {e}")