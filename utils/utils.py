'''
Author - Kaneel Senevirathne
Date - 2/19/2023
'''

from scipy.signal import argrelextrema
import yfinance as yf
import numpy as np
import pandas as pd


def get_data_yf(symbol, start, end = None):
    """
    Get data from yahoo finance given symbol, start date and end date.
    """
    return yf.download(symbol, start, end)

def normalized_values(high, low, close):
    """
    normalize the price between 0 and 1.
    """
    #epsilon to avoid deletion by 0
    epsilon = 10e-10
    
    #subtract the lows
    high = high - low
    close = close - low

    return close/(high + epsilon)

def create_targets(data, n = 10, target_winloss = [20, 0]):
    '''
    Use local min and maxes to create targets given n
    '''
    data = data.copy().reset_index(drop = False)

    #function to find how many were correct
    def locmin(row, close, target_win, target_loss):

        if (row.name + 1) == len(data):
            return pd.Series({'min': 0, 'min_value': close})

        else:

            df = data[row.name + 1:].reset_index()
            win = row.close + target_win
            stop = row.close - target_loss

            val = df.loc[(df['close'] >= win) | (df['close'] <= stop)]

            if len(val) == 0:
                return pd.Series({'min': 0, 'min_value': close})
            else:
                v = val.iloc[0]['close']

                if v <= stop:
                    out = 0
                if v >= win:
                    out = 1

            return pd.Series({'min': out, 'min_value': close})

    def locmax(row, close, target_win, target_loss):

        if (row.name + 1) == len(data):
            return pd.Series({'max': 0, 'max_value': close})

        else:            
            df = data[row.name + 1:].reset_index()
            win = row.close - target_win
            stop = row.close + target_loss

            val = df.loc[(df['close'] <= win) | (df['close'] >= stop)]

            if len(val) == 0:
                return pd.Series({'max': 0, 'max_value': close})

            else:
                v = val.iloc[0]['close']

                if v <= win:
                    out = 1
                if v >= stop:
                    out = 0

                return pd.Series({'max': out, 'max_value': close})
            

    data['loc_min'] = data.iloc[argrelextrema(data.close.values, np.less_equal, order = n)[0]]['close']
    data['loc_max'] = data.iloc[argrelextrema(data.close.values, np.greater_equal, order = n)[0]]['close']

    #get locmins and loc maxes        
    data[['min', 'min_value']] = data.apply(lambda x: locmin(x, x.close, target_winloss[0], target_winloss[1]), axis = 1)
    data[['max', 'max_value']] = data.apply(lambda x: locmax(x, x.close, target_winloss[0], target_winloss[1]), axis = 1)

    data['target'] = [1 if (x == 1) and (a > 0) else 2 if (y == 1) and (b > 0) else 0 for x, y, a, b in \
                    zip(data['min'], data['max'], data['loc_min'], data['loc_max'])]
    
    return data