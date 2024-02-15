from tqdm import tqdm
import alphas101
import pandas as pd
from sklearn import linear_model

def get_positions(symbols, path='./Data/'):
    dataset = pd.DataFrame()
    for symbol in tqdm(symbols):
        df = pd.read_csv(f'{path}{symbol}_hist.csv')
        df2 = df.copy()
        alpha = alphas101.Alphas(df2)
        dataset[symbol+'_alpha032'] = alpha.alpha032() # here we simply use alpha032 for simplicity
    dataset['timestamp'] = df2['timestamp']
    dataset.set_index('timestamp', inplace=True)
    dataset.dropna(how='all', inplace=True)
    dataset.fillna(0, inplace=True)
    rankings = dataset.rank(axis = 1, ascending=False)
    positions = rankings.map(lambda x: 1 if x <= 30 else 0) # pick the top 30 alpha values and hold one per ticker
    return positions