from toybox.src.toybox.base import ValuationInfo


class Stock:
    def __init__(self) -> None:
        self.name: str = ""
        self.ticker: str = ""
        self.valuation_info: ValuationInfo = ValuationInfo()
