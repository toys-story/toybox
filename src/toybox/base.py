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
    data = get_data(bt.client, market="KRW-ETH",from_date=[2021, 11, 27, 0, 0, 0])
    print(f"data : {len(data)} EA")
    
    stds = get_std(data=data)
    capital = 100000000
    stock = 0
    amount_stock = 0.5
    comission = 0
    buy_lines = 0
    sell_lines = 0
    print(f"Hclose by open : {stds['Hclose_by_open']}")
    print(f"Htail by close : {stds['Htail_by_close']}")
    print(f"Lclose_by_open : {stds['Lclose_by_open']}")
    print(f"Ltail_by_close : {stds['Ltail_by_close']}")
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
        elif close - open <= 0:
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
        if close-open > 0 and close_var >= buy_conditions[0] and var <= buy_conditions[1]:
            buy_amount = capital * amount_stock // close
            stock += buy_amount
            buy_money = close * buy_amount
            capital -= buy_money
            comission += (buy_money * 0.0005)
            print(f"{result}, Buy {close}, stock : {stock}, capital : {capital}")
        elif close_var >= sell_conditions[0]:
            if stock > 0:
                sell_money = stock * close
                capital += sell_money
                stock = 0
                comission += (sell_money * 0.0005)
                print(f"{result}, Sell {close} stock : {stock}, capital : {capital}")    
    capital += (close * stock)
    print(f"capital = {capital}")
    print(f"comission = {comission}")