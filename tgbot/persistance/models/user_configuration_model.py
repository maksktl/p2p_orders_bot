from sqlalchemy import sql, Column, String, Float, ARRAY
from sqlalchemy.dialects.postgresql import UUID

from tgbot.persistance.models import TimedBaseModel
from tgbot.services.dto.user_configuration_dto import UserConfigurationDto


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

    def fill(self, dto: UserConfigurationDto):
        self.user_id = dto.user_internal_id
        self.asset = dto.asset
        self.fiat = dto.fiat
        self.deposit = dto.deposit
        self.spread_to = dto.spread_to
        self.spread_from = dto.spread_from
        self.exchange_buy = dto.exchange_buy
        self.trade_type_sell = dto.trade_type_sell
        self.trade_type_buy = dto.trade_type_buy
        self.payment_sell = dto.payment_sell
        self.payment_buy = dto.payment_buy

    def update(self, dto: UserConfigurationDto):
        self.asset = dto.asset or self.asset
        self.fiat = dto.fiat or self.fiat
        self.deposit = dto.deposit or self.deposit
        self.spread_to = dto.spread_to or self.spread_to
        self.spread_from = dto.spread_from or self.spread_from
        self.exchange_buy = dto.exchange_buy or self.exchange_buy
        self.trade_type_sell = dto.trade_type_sell or self.trade_type_sell
        self.trade_type_buy = dto.trade_type_buy or self.trade_type_buy
        self.payment_sell = dto.payment_sell or self.payment_sell
        self.payment_buy = dto.payment_buy or self.payment_buy
