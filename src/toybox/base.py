import json
import os
from upbit.client import Upbit
import numpy as np

ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) 
ENV_PATH = ROOT_DIR + "/.env.json"

class baseTrader():
    def __init__(self, capital=0) -> None:
        try:
            self._get_cred()
            self.client = self._connect_upbit()
            self.account = Account(capital=capital)
            self.trade_history = [
                {
                    "type": "Buy", "time": "2019-00-00 00:00:00", 
                    "market": "KRW-XXX", "amount": 0, "price": 0
                    },
                ]
        except Exception as e:
            print(f"Error : {e}")

    def _get_cred(self) -> None:
        data = dict()
        with open(ENV_PATH, "r") as f:
            data = json.load(f)
        self.access_key = data.get("access_key", "")
        self.secret_key = data.get("secret_key", "")
        
    def _connect_upbit(self) -> Upbit:
        client = Upbit(self.access_key, self.secret_key)
        resp = client.APIKey.APIKey_info()
        
        if "error" in resp["result"]:
            raise Exception(resp["result"].get("error", None))
        return client

    def _update_trade_history(self, type="Buy", market="KRW-BTC", price=100, amount=0, time=None) -> None:
        history = {
            "type": type, "time": time, "market": market, "amount": amount, "price": price, 
            "etc": f"avg_price: {self.account.avg_price}, remain: {self.account.stock}",
        }
        self.trade_history.append(history)
        
    def show_trade_history(self) -> None:
        for t in self.trade_history:
            print(t)
    
    def buy_stock(self, market="KRW-BTC", price=100, buy_ratio=0.1, time=None, test_mode=True) -> bool:
        if self.account.remain_money <= price:
            return False
        
        amount = self.account.remain_money * buy_ratio // price
        if test_mode:
            self.account.stock += amount
            self.account.used_money += amount * price
            self.account.remain_money -= amount * price
            self.account.commision += int(amount * price * 0.0005)
            self.account.update_avg_price()
            self._update_trade_history("Buy", market, price, amount, time)
        else:
            pass
        return True
        
    def sell_stock(self, market="KRW-BTC", price=100, sell_ratio=0.1, time=None, test_mode=True) -> bool:
        if self.account.stock <= 0:
            return False

        amount = round(self.account.stock * sell_ratio, 0)
        if test_mode:
            self.account.stock -= amount
            self.account.used_money -= amount * price
            self.account.remain_money += amount * price
            self.account.commision += int(amount * price * 0.0005)
            self.account.update_avg_price()
            self._update_trade_history("Sell", market, price, amount, time)
        else:
            pass
        return True
        
class Account():
    def __init__(self, capital=0) -> None:
        self.capital = capital
        self.stock = 0
        self.avg_price = 0
        self.commision = 0
        self.used_money = 0
        self.remain_money = capital
    
    def update_avg_price(self) -> None: # weired !!! used_money don't display correct result
        if self.stock > 0:
            self.avg_price = round((self.used_money / self.stock), 1)
        else:
            self.avg_price = 0

    def show_account(self) -> None:
        revenue_before_commission = round(self.remain_money / self.capital * 100, 2) - 100
        revenue_after_commission = round((self.remain_money - self.commision) / self.capital * 100, 2) - 100
        print("-------------------------")
        print(f"Capital : {self.capital} -> {self.remain_money}")
        print(f"Commission : {self.commision}")
        print(f"Stock : {self.stock}")
        print(f"Revenue (Before Commission) : {self.remain_money}, {revenue_before_commission}%")
        print(f"Revenue (After Commission) : {self.remain_money - self.commision}, {revenue_after_commission}%")

if __name__ == '__main__':
    bt = baseTrader()