import json
import os
from upbit.client import Upbit
from libs import get_data

ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) 
ENV_PATH = ROOT_DIR + "/.env.json"

class baseTrader():
    def __init__(self):
        try:
            self._get_cred()
            self._check_connection()
            
            
        except Exception as e:
            print(f"Error : {e}")

    def _get_cred(self):
        data = dict()
        with open(ENV_PATH, "r") as f:
            data = json.load(f)
        self.access_key = data.get("access_key", "")
        self.secret_key = data.get("secret_key", "")
        
    def _check_connection(self):
        self.client = Upbit(self.access_key, self.secret_key)
        resp = self.client.APIKey.APIKey_info()
        
        if "error" in resp["result"]:
            raise Exception(resp["result"].get("error", None))
        
if __name__ == '__main__':
    bt = baseTrader()
    print(bt.client)
    # def get_data(client=None, market="KRW-BTC", type="minutes", from_date=[2021, 1, 1, 0, 0, 0], to_date=""):
    data = get_data(bt.client, from_date=[2021, 11, 23, 14, 0, 0])
    print(len(data))
    data.reverse()
    for d in data:
        open = float(d.get("opening_price", ""))
        close = float(d.get("trade_price", ""))
        high = float(d.get("high_price", ""))
        low = float(d.get("low_price", ""))
        time = d.get("candle_date_time_kst", "")
        candle = "Plus" if close-open > 0 else "Minus"
        result = f"{time}, {candle}, +{high-open}, -{open-low}"
        print(result)
