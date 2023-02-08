from sqlalchemy import sql, Column, String
from sqlalchemy.dialects.postgresql import UUID

from tgbot.persistance.models import TimedBaseModel


class StepModel(TimedBaseModel):
    __tablename__ = 'step'
    query: sql.Select

    user_id = Column(UUID, nullable=False, index=True)
    strategy_type = Column(String(8), nullable=False)
    order_id = Column(UUID, nullable=False)
    next_step_id = Column(UUID)

