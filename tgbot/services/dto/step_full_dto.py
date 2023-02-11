from dataclasses import dataclass
from uuid import UUID

from tgbot.persistance.models import StepModel
from tgbot.services.dto.order_full_dto import OrderFullDto


@dataclass
class StepFullDto:
    id: UUID
    user_id: UUID
    strategy_type_buy: str
    strategy_type_sell: str
    order_buy: OrderFullDto
    order_sell: OrderFullDto

    def __init__(self, step: StepModel):
        self.user_id = step.user_id
        self.strategy_type_buy = step.strategy_type_buy
        self.strategy_type_sell = step.strategy_type_sell
        self.order_buy = OrderFullDto(step.order_buy)
        self.order_sell = OrderFullDto(step.order_sell)
