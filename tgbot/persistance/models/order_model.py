from sqlalchemy import sql, Column, Text, String, ARRAY, INTEGER, UniqueConstraint, DECIMAL

from tgbot.persistance.models import TimedBaseModel


class OrderModel(TimedBaseModel):
    __tablename__ = 'stock_order'
    query: sql.Select
    __table_args__ = (
        UniqueConstraint('external_id', 'source', name='uq_stock_order_external_id_source'),
    )

    external_id = Column(Text, nullable=False, index=True)
    username = Column(Text, nullable=False)
    source = Column(String(32), nullable=False, index=True)
    asset = Column(String(8), nullable=False, index=True)
    fiat = Column(String(8), nullable=False)
    price = Column(DECIMAL(14, 2), nullable=False, index=True)
    trade_type = Column(String(4), nullable=False)
    limit_lower = Column(DECIMAL(14, 2), nullable=False)
    limit_upper = Column(DECIMAL(14, 2), nullable=False)
    capital = Column(DECIMAL(14, 2))
    pay_type = Column(ARRAY(String), nullable=False, default=[])
    partition = Column(INTEGER, default=1, index=True)
