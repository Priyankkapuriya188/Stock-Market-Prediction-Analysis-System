import pandas as pd
import numpy as np

def calculate_features(df):
    
    df['ma5'] = df['Close'].rolling(5).mean()
    df['ma20'] = df['Close'].rolling(20).mean()
    
    df['ema12'] = df['Close'].ewm(span = 12, adjust = False).mean()
    df['ema26'] = df['Close'].ewm(span = 26, adjust = False).mean()
    
    delta = df['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()
    
    rs = avg_gain / avg_loss
    df['rsi'] = 100 - (100/(1+rs))
    
    df['macd'] = df['ema12'] - df['ema26']
    df['macd_signal'] = df['macd'].ewm(span = 9, adjust = False).mean()
    
    df['return'] = df['Close'].pct_change()
    df['volatility'] = df['return'].rolling(10).std()
    
    df['close_lag1'] = df['Close'].shift(1)
    df['return_lag1'] = df['return'].shift(1)
    
    # Time zone proper hovathi hour/minute Indian time pramane j aavse
    df['hour'] = df.index.hour
    df['minute'] = df.index.minute
    
    df['target_return'] = df['return'].shift(-1)
    df['trend'] = np.where(df['target_return'].isna(), np.nan, (df['target_return'] > 0).astype(int))
    
    df['volume_sma'] = df['Volume'].rolling(20).mean()
    df['volume_spike'] = np.where(df['Volume'] > (df['volume_sma']  * 2), 1, 0)
    df.drop(columns=['volume_sma'], inplace=True)
    
    return df