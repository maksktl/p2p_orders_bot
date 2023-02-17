from dataclasses import dataclass
from typing import List
from uuid import UUID


@dataclass
class UserConfigurationDto:
    asset: List[str]
    fiat: str
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
    user_internal_id: UUID = None

    def __init__(self):
        self.asset = None
        self.fiat = None
        self.deposit = None
        self.spread_from = None
        self.spread_to = None
        self.exchange_sell = None
        self.exchange_buy = None
        self.trade_type_sell = None
        self.trade_type_buy = None
        self.payment_sell = None
        self.payment_buy = None

    def __init__(self, payload: dict):
        self.asset = payload.get('cryptoSend', [])
        self.fiat = payload.get('fiatSend', '')
        self.deposit = float(payload.get('deposit', 0.0))
        self.spread_from = float(payload.get('spreadFrom', 0.0))
        self.spread_to = float(payload.get('spreadTo', 0.0))
        self.exchange_sell = payload.get('cryptoAggregatorsSend', [])
        self.exchange_buy = payload.get('cryptoAggregatorsSend1', [])
        self.trade_type_sell = 'maker' if (payload.get('makerTaker', 'Мейкер')).lower() == 'мейкер' else 'taker'
        self.trade_type_buy = 'maker' if (payload.get('makerTaker1', 'Мейкер')).lower() == 'мейкер' else 'taker'
        self.payment_sell = payload.get('banksSend', [])
        self.payment_buy = payload.get('banksSend1', [])
