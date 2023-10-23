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

def create_volume_bar(data, thresh = 2000):
    
    df = data.copy()
    
    #create volume bars
    df_resampled = df.resample('1T', on='date').agg({'open': 'first', 'high': 'max', 'close': 'last', 'low': 'min', 'volume': 'sum'}).fillna(0).reset_index()

    # Create a new dataframe to store the resampled values when volume accumulates 1000 units
    df_new = pd.DataFrame(columns=['open', 'high', 'close', 'low', 'delta', 'o_index', 'date'])

    #volume threshold
    vol_thresh = thresh

    #initial values
    volume_accumulated = 0
    start_time = None

    # Iterate over each row in the resampled dataframe
    for index, row in df_resampled.iterrows():
        volume_accumulated += row['volume']

        if volume_accumulated >= vol_thresh:
            # Calculate the time difference since the last 1000 volume accumulation
            delta = (index - start_time) if start_time else 0

            # Append a new row to the new dataframe
            df_new.loc[index] = [row['open'], row['high'], row['close'], row['low'], delta, index, row['date']]

            # Reset the volume accumulator and start time for the next accumulation
            volume_accumulated = 0
            start_time = None

        if volume_accumulated < vol_thresh and start_time is None:
            # Set the start time when the volume accumulation starts
            start_time = index
            
    return df_new

def generate_trends(data):
    
    data['trend'] = 0
    data['trend_strength'] = np.nan
    data['trend_period'] = np.nan
    
    targets = data['target'].values

    min_indices = np.where(targets == 1)[0]

    max_indices = np.where(targets == 2)[0]

    ind_dict = {}

    for i in min_indices:
        ind_dict[i] = 1

    for i in max_indices:
        ind_dict[i] = 2

    sorted_dict = {k: ind_dict[k] for k in sorted(ind_dict)}

    current_ind = next(iter(sorted_dict))
    current_trend = sorted_dict[current_ind]


    for i, trend in sorted_dict.items():

        if current_trend == trend:
            continue
        elif (current_trend == 1) and (trend == 2):
            data.loc[current_ind:i, 'trend'] = 1
            
            trend_strength = 1 - ((np.arange(current_ind, i, 1) - current_ind) / (i - current_ind))
            
            data.loc[np.arange(current_ind, i, 1), 'trend_strength'] = trend_strength.tolist()
            
            data.loc[current_ind:i, 'trend_period'] = (i - current_ind)
            
            current_ind = i
            current_trend = trend
        elif (current_trend == 2) and (trend == 1):
            data.loc[current_ind:i, 'trend'] = 2
            
            trend_strength = 1 - ((np.arange(current_ind, i, 1) - current_ind) / (i - current_ind))
            
            data.loc[np.arange(current_ind, i, 1), 'trend_strength'] = trend_strength.tolist()
            
            data.loc[current_ind:i, 'trend_period'] = (i - current_ind)
            
            current_ind = i
            current_trend = trend
            
    return data