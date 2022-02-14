from abc import ABCMeta


class ValuationInfo():
    def __init__(self) -> None:
        self.purchase_amount: float = 0
        self.rate_of_return: float = 0
        self.evaluated_amount: float = 0
        self.evaluated_pnl: float = 0

class BaseTrader(metaclass=ABCMeta):
