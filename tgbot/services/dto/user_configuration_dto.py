from dataclasses import dataclass
from typing import List
from uuid import UUID


@dataclass
class UserConfigurationDto:
    asset: List[str]
    fiat: str
    deposit: int
    spreadFrom: int
    spreadTo: int
    exchangeSell: List[str]
    exchangeBuy: List[str]
    tradeTypeSell: str
    tradeTypeBuy: str
    paymentSell: List[str]
    paymentBuy: List[str]
    id: UUID = None
    userId: UUID = None

    def __init__(self):
        self.asset = None
        self.fiat = None
        self.deposit = None
        self.spreadFrom = None
        self.spreadTo = None
        self.exchangeSell = None
        self.exchangeBuy = None
        self.tradeTypeSell = None
        self.tradeTypeBuy = None
        self.paymentSell = None
        self.paymentBuy = None

    def __init__(self, payload: dict):
        self.asset = payload.get('cryptoSend', [])
        self.fiat = payload.get('fiatSend', '')
        self.deposit = int(float(payload.get('deposit', 0.0))*100)
        self.spreadFrom = int(float(payload.get('spreadFrom', 0.0)) * 100)
        self.spreadTo = int(float(payload.get('spreadTo', 0.0)) * 100)
        self.exchangeSell = payload.get('cryptoAggregatorsSend1', [])
        self.exchangeBuy = payload.get('cryptoAggregatorsSend', [])
        self.tradeTypeSell = 'maker' if (payload.get('makerTaker1', 'Мейкер')).lower() == 'мейкер' else 'taker'
        self.tradeTypeBuy = 'maker' if (payload.get('makerTaker', 'Мейкер')).lower() == 'мейкер' else 'taker'
        self.paymentSell = payload.get('banksSend1', [])
        self.paymentBuy = payload.get('banksSend', [])
