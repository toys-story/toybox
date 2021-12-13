
from toybox.src.toybox.decorator import logging


class Account():
    def __init__(self, capital=0) -> None:
        self._capital = capital
        self._stock = {"KRW-BTC": {"amount": 0, "avg_price": 0}}
        self._commision = 0
        self._used_money = 0
        self._remain_money = capital

    @property
    def remain_money(self):
        return self._remain_money
    
    @property
    def stock(self):
        return self._stock

    def get_avg_price(self, market="KRW-BTC") -> int:
        return self._stock.get(market, {}).get("avg_price", 0)
    
    def get_having_amount(self, market="KRW-BTC") -> int:
        return self._stock.get(market, {}).get("amount", 0)
    
    @logging
    def update_account_info(self, market="", amount=0, price=0) -> None: 
        if not market or not amount or not price:
            print(f"Error : {market}, {amount}, {price}")
            raise RuntimeError("Error : invaild data")
        
        stock_info = self._stock.get(market, {})
        order_money = amount * price

        if amount > 0:  # Buy
            if self._remain_money < order_money:
                raise RuntimeError(f"Error : lack of money(remain:{self._remain_money}, order:{order_money}")

            if stock_info:
                balance = stock_info["amount"] * stock_info["avg_price"]
                order_money = amount * price
                stock_info["avg_price"] = (balance + order_money) / (stock_info["amount"] + amount)
            else:
                self._stock[market] = {"amount": amount, "avg_price": price}
        else:  # Sell
            if stock_info:
                if (having := self.get_having_amount(market=market)) < amount:
                    raise RuntimeError(f"Error : lack of amount(having:{having}, order:{amount}")
            else:
                print(f"Error : {market}, {amount}, {price}")
                raise RuntimeError("Error : invaild data")

        self._remain_money -= order_money
        self._used_money += order_money
        self._commision += int(abs(amount) * price * 0.0005)
        if stock_info:
            self._stock[market]["amount"] += amount


    def show_account(self) -> None:
        revenue_before_commission = round(self._remain_money / self._capital * 100 - 100, 2)
        revenue_after_commission = round((self._remain_money - self._commision) / self._capital * 100 - 100, 2)
        print("-------------------------")
        print(f"Capital : {self._capital} -> {self._remain_money}")
        print(f"Commission : {self._commision}")
        print(f"Stock : {self._stock}")
        print(f"Revenue (Before Commission) : {self._remain_money}, {revenue_before_commission}%")
        print(f"Revenue (After Commission) : {self._remain_money - self._commision}, {revenue_after_commission}%")
