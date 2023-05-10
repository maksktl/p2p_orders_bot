from dataclasses import dataclass
from typing import List
from uuid import UUID

from tgbot.services.dto import UserFullDto


@dataclass
class UserConfigurationFullDto:
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
    user_id: UUID
    user: UserFullDto
    deleted: bool
    id: UUID = None

    def __init__(self, payload: dict):
        self.user_id = payload.get('userId', None)
        self.asset = payload.get('asset', None)
        self.fiat = payload.get('fiat', None)
        self.deposit = payload.get('deposit', None)
        self.spread_from = payload.get('spreadFrom', None)
        self.spread_to = payload.get('spreadTo', None)
        self.exchange_sell = payload.get('exchangeSell', None)
        self.exchange_buy = payload.get('exchangeBuy', None)
        self.trade_type_sell = payload.get('tradeTypeSell', None)
        self.trade_type_buy = payload.get('tradeTypeBuy', None)
        self.payment_sell = payload.get('paymentSell', None)
        self.payment_buy = payload.get('paymentBuy', None)
        self.id = payload.get('id', None)
        self.deleted = payload.get('deleted', None)
