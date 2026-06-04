import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import mysql.connector
import warnings
import time
from datetime import datetime
warnings.filterwarnings('ignore')

def main():
    now = datetime.now()
    secondPassed = (now.minute % 5) * 60 + now.second
    secondToWait = 300 - secondPassed
    totalWait = secondToWait + 60
    nextRunTime = datetime.fromtimestamp(time.time() + totalWait)
    print(f"Waiting for next candle... Script will automatically run at {nextRunTime.strftime('%I:%M:%S %p')}")
    time.sleep(totalWait)
    
    while True:
        try:
            conn = mysql.connector.connect(host='localhost', user='root', password='', db='mydatabase')
            df = pd.read_sql("SELECT * FROM stock_price_predict", conn)
            conn.close()

            if df.empty or 'trend' not in df.columns:
                exit("Database is empty or missing 'trend' column.")

            features = [col for col in df.columns if col not in ['datetime', 'symbol', 'trend', 'id']]
            X, y = df[features], df['trend']
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

            model = xgb.XGBClassifier(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42).fit(X_train, y_train)

            latest = df.sort_values(by='datetime', ascending=False).iloc[[0]]
            pred = model.predict(latest[features])[0]

            print(f"{latest['symbol'].iloc[0]} | {latest['datetime'].iloc[0]} | {'BULLISH 📈' if pred==1 else 'BEARISH 📉'}")
            time.sleep(300)
        except Exception as e:
            print('Error:', e)
            time.sleep(300)

if __name__ == '__main__':
    main()