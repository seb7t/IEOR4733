import pandas as pd
from tqdm import tqdm
import numpy as np
import os
import shutil

def data_download(api, symbols, timeframe, start_date, end_date, path = './Data/'):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)

    for symbol in tqdm(symbols):
        # Fetch historical market data
        historical_data = api.get_bars(symbol, timeframe, start=start_date, end=end_date).df
        csv_filename = f'{symbol}_hist.csv'
        historical_data.to_csv(path + csv_filename, index=True)