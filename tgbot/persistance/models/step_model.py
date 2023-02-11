from sqlalchemy import sql, Column, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID

from tgbot.persistance.models import TimedBaseModel


class StepModel(TimedBaseModel):
    __tablename__ = 'step'
    __table_args__ = (
        UniqueConstraint('user_id', 'order_buy_id', 'order_sell_id', name='uq_user_buy_sell'),
    )

    query: sql.Select
    user_id = Column(UUID, nullable=False, index=True)
    strategy_type_buy = Column(String(8), nullable=False)
    strategy_type_sell = Column(String(8), nullable=False)
    order_buy_id = Column(UUID, nullable=False, index=True)
    order_sell_id = Column(UUID, nullable=False, index=True)

    def fill(self, **kwargs):
        self.user_id = kwargs.get('user_id')
        self.strategy_type_buy = kwargs.get('strategy_type_buy')
        self.strategy_type_sell = kwargs.get('strategy_type_sell')
        self.order_buy_id = kwargs.get('order_buy_id')
        self.order_sell_id = kwargs.get('order_sell_id')
