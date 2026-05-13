import mysql.connector
import yfinance as yf
from calculateFeatures import calculate_features
import pandas as pd
import numpy as np

# Database connection
conn = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '',
    db = 'mydatabase'
)

cursor = conn.cursor()

# Symbol declare karyo chhe
symbol = 'RELIANCE.NS'

def fatch_and_store():
    df = yf.download(symbol, interval='5m', period='5d')
    
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(1)
    
    if df.empty:
        print(f"No data received for {symbol}. Skipping...")
        return
    
    # Timezone Fix
    if df.index.tz is None:
        df.index = df.index.tz_localize('UTC')
    df.index = df.index.tz_convert('Asia/Kolkata')
    df.index = df.index.tz_localize(None)
    
    # Calculate Features
    df = calculate_features(df)
    df = df.dropna(subset=['rsi', 'ma20'])
    
    # Last 2 closed candles
    latest = df.iloc[-3:-1]
    
    values_list = []
        
    for index, row in latest.iterrows():
        dt = index.to_pydatetime() 
        row = row.replace({np.nan: None}) 

        values_list.append(( 
            dt, symbol, row['Open'], row['High'], row['Low'], row['Close'], 
            row['Volume'], row['ma5'], row['ma20'], row['ema12'], 
            row['ema26'], row['rsi'], row['macd'], row['macd_signal'], 
            row['return'], row['volatility'], row['close_lag1'], 
            row['return_lag1'], row['hour'], row['minute'], 
            row['trend'], row['target_return'], row['volume_spike']
        ))
        
    # --- UPDATE 2: Query ma 'symbol' ane teno '%s' add karyo ---
    query = """
        INSERT INTO stock_price_predict (
            datetime, symbol, open, high, low, close, volume,
            ma5, ma20, ema12, ema26,
            rsi, macd, macd_signal,
            `return`, volatility, close_lag1, return_lag1,
            hour, minute, trend, target_return, volume_spike
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            close = VALUES(close),
            volume = VALUES(volume),
            target_return = VALUES(target_return),
            trend = VALUES(trend),
            volume_spike = VALUES(volume_spike)
        """

    cursor.executemany(query, values_list)
    conn.commit()
    
    print(f"[{symbol}] Data stored successfully with symbol column!")