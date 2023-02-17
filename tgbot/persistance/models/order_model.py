from email.policy import default

from sqlalchemy import sql, Column, Text, String, Float, ARRAY, INTEGER, UniqueConstraint

from tgbot.persistance.models import TimedBaseModel


class OrderModel(TimedBaseModel):
    __tablename__ = 'stock_order'
    query: sql.Select
    __table_args__ = (
        UniqueConstraint('external_id', 'source', name='uq_stock_order_external_id_source'),
    )

    external_id = Column(Text, nullable=False)
    username = Column(Text, nullable=False)
    source = Column(String(32), nullable=False)
    asset = Column(String(8), nullable=False)
    fiat = Column(String(8), nullable=False)
    price = Column(Float(precision=2), nullable=False)
    trade_type = Column(String(4), nullable=False)
    limit_lower = Column(Float(precision=2), nullable=False)
    limit_upper = Column(Float(precision=2), nullable=False)
    capital = Column(Float(precision=2))
    pay_type = Column(ARRAY(String), nullable=False, default=[])
    partition = Column(INTEGER, default=1)
