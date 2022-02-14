from toybox.src.toybox.stock import Stock
from toybox.src.toybox.base import ValuationInfo


class Account:
    def __init__(self) -> None:
        self.initial_asset: float = 0  # 초기 투자금 : 처음 투자 시작한 금액
        self.stock: Stock = None  # 주식 정보 : 보유한 주식 정보
        self.valuation_info: ValuationInfo = ValuationInfo()  # 세부 정보 : 현 계좌의 세부 정보
        self.orderable_amount: float = 0  # 예수금 : 주문 가능 금액
        self.estimate_asset: float = 0  # 추정 자산 : 평가금액 + 예수금
