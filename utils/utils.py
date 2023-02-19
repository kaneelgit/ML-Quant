'''
Author - Kaneel Senevirathne
Date - 2/19/2023
'''


import yfinance as yf



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