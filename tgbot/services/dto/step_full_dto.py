from dataclasses import dataclass
from uuid import UUID

from tgbot.services.dto.order_full_dto import OrderFullDto


@dataclass
class StepFullDto:
    id: UUID
    user_id: UUID
    strategy_type_buy: str
    strategy_type_sell: str
    order_buy: OrderFullDto
    order_sell: OrderFullDto
    spread: int

    def __init__(self, payload: dict):
        self.user_id = payload.get('userId', None)
        self.strategy_type_buy = payload.get('strategyTypeBuy', None)
        self.strategy_type_sell = payload.get('strategyTypeSell', None)
        self.order_buy = payload.get('orderBuy', None)
        self.order_sell = payload.get('orderSell', None)
        self.spread = payload.get('spread', None)
