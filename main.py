from database import fatch_and_store
import time
from datetime import datetime

def main():
    print("Stock Data Pipeline Started. Running every 5 minutes...")
    now = datetime.now()
    secondPassed = (now.minute % 5) * 60 + now.second
    secondToWait = 300 - secondPassed
    totalWait = secondToWait + 60
    nextRunTime = datetime.fromtimestamp(time.time() + totalWait)
    print(f"Waiting for next candle... Script will automatically run at {nextRunTime.strftime('%I:%M:%S %p')}")
    time.sleep(totalWait)
    
    while True:
        try:
            fatch_and_store()
            # 5 minute = 300 seconds
            time.sleep(300)
        except Exception as e:
            print('Error occurred:', e)
            # Jo internet issues ke api limit ni error aave, to pan script bandh na thay
            time.sleep(300)
    
if __name__ == '__main__':
    main()