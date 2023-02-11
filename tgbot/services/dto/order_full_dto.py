from typing import List

from tgbot.persistance.models.order_model import OrderModel


@dataclass
class OrderFullDto:
    id: UUID
    external_id: str
    username: str
    source: str
    asset: str
    fiat: str
    price: float
    trade_type: str
    limit_lower: float
    limit_upper: float
    capital: float
    pay_type: List[str]

    def __init__(self, order_model: OrderModel):
        self.id = order_model.id
        self.external_id = order_model.external_id
        self.username = order_model.username
        self.source = order_model.source
        self.asset = order_model.asset
        self.fiat = order_model.fiat
        self.price = order_model.price
        self.trade_type = order_model.trade_type
        self.limit_lower = order_model.limit_lower
        self.limit_upper = order_model.limit_upper
        self.capital = order_model.capital
        self.pay_type = order_model.pay_type
