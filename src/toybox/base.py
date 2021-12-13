import json
import os
from upbit.client import Upbit
import abc
from .account import Account
from .decorator import logging

ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) 
ENV_PATH = ROOT_DIR + "/.env.json"

class baseTrader(metaclass=abc.ABCMeta):
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

    @logging
    def _get_cred(self) -> None:
        data = dict()
        with open(ENV_PATH, "r") as f:
            data = json.load(f)
        self.access_key = data.get("access_key", "")
        self.secret_key = data.get("secret_key", "")
        
    @logging
    def _connect_upbit(self) -> Upbit:
        client = Upbit(self.access_key, self.secret_key)
        resp = client.APIKey.APIKey_info()
        
        if "error" in resp["result"]:
            raise Exception(resp["result"].get("error", None))
        return client

    def _update_trade_history(self,market="KRW-BTC", price=100, amount=0, time=None) -> None:
        type = "BUY" if amount > 0 else "SELL"
        history = {
            "type": type, "time": time, "market": market, "amount": amount, "price": price, 
            "etc": f"avg_price: {self.account.get_avg_price(market=market)}, remain: {self.account.stock}",
        }
        self.trade_history.append(history)
    
    def show_trade_history(self) -> None:
        for t in self.trade_history:
            print(t)
    
    @abc.abstractmethod
    def check_conditions(self, data) -> str:
        print(f"Error : abs method used {self.check_conditions.__name__}")
        raise RuntimeError(f"abs method used {self.check_conditions.__name__}")

    @logging
    def buy_stock(self, market="KRW-BTC", price=100, buy_ratio=0.1, time=None, test_mode=True) -> bool:
        if (remain_money := self.account.remain_money) <= price:
            print(f"Info : Can't buy anymore, remain:{remain_money}, price:{price}")
            return False

        if (amount := (remain_money * buy_ratio // price)) <= 0:
            print(f"Info : remaining money is under {buy_ratio}, remain:{remain_money}, price:{price}")
            return False
        
        try:
            if test_mode:
                self.account.update_account_info(market=market, amount=amount, price=price)
                self._update_trade_history(market, price, amount, time)
            else:
                pass
        except Exception as e:
            print(f"Error : {e}")
            return False
        return True
        
    @logging
    def sell_stock(self, market="KRW-BTC", price=100, sell_ratio=0.1, time=None, test_mode=True) -> bool:
        if (having := self.account.get_having_amount(market=market)) <= 0:
            print(f"Info : Can't sell, having:{having}")
            return False
        if (amount := round(having * sell_ratio, 0)) <= 0:
            return False
        amount = amount * (-1)
        try:
            if test_mode:
                self.account.update_account_info(market=market, amount=amount, price=price)
                self._update_trade_history(market, price, amount, time)
            else:
                pass
        except Exception as e:
            print(f"Error : {e}")
            return False
        return True
        

if __name__ == '__main__':
    bt = baseTrader()