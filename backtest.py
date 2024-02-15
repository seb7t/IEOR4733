import alpaca_trade_api as tradeapi
import pandas as pd
from collections import defaultdict
from matplotlib import pyplot as plt
import data_prep
import strategy
from tqdm import tqdm

def backtest(symbols, api):
    timeframe = tradeapi.TimeFrame.Day
    end_date = '2024-02-01'
    start_date = '2023-01-01'
    data_prep.data_download(api, symbols.tolist()+['QQQ'], timeframe, start_date, end_date, path='./Data_BT/')
    positions = strategy.get_positions(symbols, path='./Data_BT/')
    dfs = defaultdict()
    for symbol in tqdm(symbols):
        df = pd.read_csv(f'./Data_BT/{symbol}_hist.csv')
        df.set_index('timestamp', inplace=True)
        dfs[symbol] = df
    bt = pd.DataFrame(index = positions.index)
    bt['holdings'] = 0.00
    bt['cash'] = 0.00
    for index in tqdm(bt.index.to_list()):
        i = bt.index.get_loc(index)
        for symbol in symbols:
            j = positions.columns.get_loc(symbol+'_alpha032')
            if positions.iloc[i, j] == 0:
                if i != 0 and positions.iloc[i-1, j] != 0:
                    bt.loc[index, 'cash'] += positions.iloc[i-1, j] * dfs[symbol].loc[index, 'close']
            else:
                bt.loc[index, 'holdings'] += positions.iloc[i, j] * dfs[symbol].loc[index, 'close']
                if i == 0 or positions.iloc[i-1, j] == 0:
                    bt.loc[index, 'cash'] -= positions.iloc[i, j] * dfs[symbol].loc[index, 'close']
    bt['cash'] -= bt['cash'].iloc[0]
    bt['total'] = bt['holdings'] + bt['cash']
    bt['return'] = bt['total']/bt['total'].shift(1) - 1
    bt['return_cum'] = bt['total']/bt['total'].iloc[0] - 1

    qqq = pd.read_csv(f'./Data_BT/QQQ_hist.csv')
    qqq.set_index('timestamp', inplace=True)
    bt['qqq'] = qqq.loc[bt.index, 'close'] * 30
    bt['total_qqq'] = bt['qqq']
    bt['return_qqq'] = bt['total_qqq']/bt['total_qqq'].shift(1) - 1
    bt['return_qqq_cum'] = bt['total_qqq'] / bt['total_qqq'].iloc[0] - 1

    fig, axs = plt.subplots(2, 1, figsize=(14, 7))
    axs[0].plot(bt.index, bt['return'], label='alpha_032', color='orange')
    axs[0].plot(bt.index, bt['return_qqq'], label='NASDAQ', color='blue')
    axs[0].set_xlabel('Date')
    axs[0].set_title('Return')
    axs[0].legend()

    axs[1].plot(bt.index, bt['return_cum'], label='alpha_032', color='orange')
    axs[1].plot(bt.index, bt['return_qqq_cum'], label='NASDAQ', color='blue')
    axs[1].set_xlabel('Date')
    axs[1].set_title('Cumulative Return')
    axs[1].legend()

    plt.tight_layout()
    plt.show()





