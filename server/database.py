import logging
from datetime import datetime
from typing import List

import sqlalchemy as sa
from gino import Gino
from gino.schema import GinoSchemaVisitor
from sqlalchemy import Column, sql, Text, String, Float, ARRAY
from sqlalchemy.dialects.postgresql import UUID

db = Gino()
logger = logging.getLogger(__name__)


class BaseModel(db.Model):
    __abstract__ = True
    id = Column(UUID, primary_key=True, default=db.func.uuid_generate_v4())
    deleted = Column(db.Boolean, default=False)

    def __str__(self):
        model = self.__class__.__name__
        table: sa.Table = sa.inspect(self.__class__)
        primary_key_columns: List[sa.Column] = table.primary_key.columns
        values = {
            column.name: getattr(self, self._column_name_map[column.name])
            for column in primary_key_columns
        }
        values_str = " ".join(f"{name}={value!r}" for name, value in values.items())
        return f"<{model} {values_str}>"


class TimedBaseModel(BaseModel):
    __abstract__ = True

    created_at = db.Column(db.DateTime(True), server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime(True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        server_default=db.func.now(),
    )


class OrderModel(TimedBaseModel):
    __tablename__ = 'stock_order'
    query: sql.Select

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


async def shutdown():
    bind = db.pop_bind()
    if bind:
        logger.info("Close PostgreSQL Connection")
        await bind.close()


async def setup(uri):
    logger.info("Setup PostgreSQL connection")
    logging.getLogger('gino.engine._SAEngine').setLevel(logging.ERROR)
    await db.set_bind(uri)

    # Create tables
    db.gino: GinoSchemaVisitor
    # await db.gino.drop_all()  # Drop the db
    # await db.gino.create_all()
