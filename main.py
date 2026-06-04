from database import fatch_and_store
import time
from datetime import datetime

def main():
    print("Stock Data Pipeline Started. Running every 5 minutes...")
    now = datetime.now()
    secondPassed = (now.minute % 5) * 60 + now.second
    secondToWait = 300 - secondPassed
    totalWait = secondToWait + 30
    nextRunTime = datetime.fromtimestamp(time.time() + totalWait)
    print(f"Waiting for next candle... Script will automatically run at {nextRunTime.strftime('%I:%M:%S %p')}")
    time.sleep(totalWait)
    
    while True:
        try:
            fatch_and_store()
            time.sleep(300)
        except Exception as e:
            print('Error occurred:', e)
            time.sleep(300)
    
if __name__ == '__main__':
    main()