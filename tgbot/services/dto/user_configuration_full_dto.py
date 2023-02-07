from dataclasses import dataclass
from typing import List
from uuid import UUID


@dataclass
class UserConfigurationFullDto:
    asset: List[str]
    fiat: List[str]
    deposit: float
    spread_from: float
    spread_to: float
    exchange_sell: List[str]
    exchange_buy: List[str]
    trade_type_sell: str
    trade_type_buy: str
    payment_sell: List[str]
    payment_buy: List[str]
    id: UUID = None

    def __init__(self, model):
        self.asset = model.asset
        self.fiat = model.fiat
        self.deposit = model.deposit
        self.spread_from = model.spread_from
        self.spread_to = model.spread_to
        self.exchange_sell = model.exchange_sell
        self.exchange_buy = model.exchange_buy
        self.trade_type_sell = model.trade_type_sell
        self.trade_type_buy = model.trade_type_buy
        self.payment_sell = model.payment_sell
        self.payment_buy = model.payment_buy
        self.id = model.id
