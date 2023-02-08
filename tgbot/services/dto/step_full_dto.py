from dataclasses import dataclass
from uuid import UUID

from tgbot.persistance.models import StepModel


@dataclass
class StepFullDto:
    id: UUID
    user_id: UUID
    strategy_type: str
    order_id: UUID
    next_step_id: UUID

    def __init__(self, step: StepModel):
        self.user_id = step.user_id
        self.strategy_type = step.strategy_type
        self.order_id = step.order_id
        self.next_step_id = step.next_step_id
        self.id = step.id
