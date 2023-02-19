from sqlalchemy import sql, Column, String, ARRAY, Numeric
from sqlalchemy.dialects.postgresql import UUID

from tgbot.persistance.models import TimedBaseModel, UserModel
from tgbot.services.dto.user_configuration_dto import UserConfigurationDto


class UserConfigurationModel(TimedBaseModel):
    __tablename__ = 'user_configuration'
    query: sql.Select

    user_id = Column(UUID, nullable=False)
    asset = Column(ARRAY(String), nullable=False)
    fiat = Column(String(8), nullable=False)
    deposit = Column(Numeric, nullable=False)
    spread_from = Column(Numeric, nullable=False)
    spread_to = Column(Numeric, nullable=False)
    exchange_sell = Column(ARRAY(String), nullable=False, default=[])
    exchange_buy = Column(ARRAY(String), nullable=False, default=[])
    trade_type_sell = Column(String(8), nullable=False)
    trade_type_buy = Column(String(8), nullable=False)
    payment_sell = Column(ARRAY(String), nullable=False, default=[])
    payment_buy = Column(ARRAY(String), nullable=False, default=[])
    user: UserModel = None

    def fill(self, dto: UserConfigurationDto):
        self.user_id = dto.user_internal_id
        self.asset = dto.asset
        self.fiat = dto.fiat
        self.deposit = dto.deposit
        self.spread_to = dto.spread_to
        self.spread_from = dto.spread_from
        self.exchange_buy = dto.exchange_buy
        self.exchange_sell = dto.exchange_sell
        self.trade_type_sell = dto.trade_type_sell
        self.trade_type_buy = dto.trade_type_buy
        self.payment_sell = dto.payment_sell
        self.payment_buy = dto.payment_buy
