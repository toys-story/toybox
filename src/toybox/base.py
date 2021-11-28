import json
import os
from upbit.client import Upbit
from libs import get_data, get_std
import numpy as np

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
    data = get_data(bt.client, market="KRW-SAND",from_date=[2021, 11, 25, 8, 0, 0])
    print(f"data : {len(data)} EA")
    
    stds = get_std(data=data)    
    capital = 1000000
    stock = 0
    buy_lines = 0
    sell_lines = 0
    for d in data:
        open = float(d.get("opening_price", ""))
        close = float(d.get("trade_price", ""))
        high = float(d.get("high_price", ""))
        low = float(d.get("low_price", ""))
        time = d.get("candle_date_time_kst", "")
        if close-open > 0:
            close_var = (close - open) / open * 100
            var = ((high - open) / open) * 100
            var -= close_var
        elif close - open < 0:
            close_var = (close - open) / open * (-100)
            var = ((low - open) / open) * (-100)
            var -= close_var
        result = f"{time}, 변동률 : {round(close_var , 2)}, 고/저점 편차 : {round(var, 2)}"
        
        buy_conditions = [
            stds["Hclose_by_open"] * 100,
            stds["Htail_by_close"] * 100,
        ]
        sell_conditions = [
            stds["Lclose_by_open"] * 100,
            stds["Ltail_by_close"] * 100,
        ]
        if close_var >= buy_conditions[0] and var <= buy_conditions[1]:
            stock += 1
            capital -= close
            print(f"{result}, Buy {close}, stock : {stock}, capital : {capital}")
        if close_var >= sell_conditions[0] and var <= sell_conditions[1]:
            if stock > 0:
                capital += (stock * close)
                stock = 0
                print(f"{result}, Sell {close} stock : {stock}, capital : {capital}")    
    capital += (close * stock)
    print(f"capital = {capital}")