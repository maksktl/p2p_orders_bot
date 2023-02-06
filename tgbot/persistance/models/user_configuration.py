from sqlalchemy import sql, Column, String, Float, ARRAY
from sqlalchemy.dialects.postgresql import UUID

from tgbot.persistance.models import TimedBaseModel


class UserConfigurationModel(TimedBaseModel):
    __tablename__ = 'user_configuration'
    query: sql.Select

    user_id = Column(UUID, nullable=False)
    asset = Column(ARRAY(String), nullable=False)
    fiat = Column(ARRAY(String), nullable=False)
    deposit = Column(Float(precision=6), nullable=False)
    spread_from = Column(Float(precision=6), nullable=False)
    spread_to = Column(Float(precision=6), nullable=False)
    exchange_sell = Column(ARRAY(String), nullable=False, default=[])
    exchange_buy = Column(ARRAY(String), nullable=False, default=[])
    trade_type_sell = Column(String(8), nullable=False)
    trade_type_buy = Column(String(8), nullable=False)
    payment_sell = Column(ARRAY(String), nullable=False, default=[])
    payment_buy = Column(ARRAY(String), nullable=False, default=[])
