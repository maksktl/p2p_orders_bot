from typing import Optional

from tgbot.persistance import db
from tgbot.persistance.models import UserConfigurationModel, UserModel
from sqlalchemy import text


class UserConfigurationRepository:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = UserConfigurationRepository()
        return cls._instance

    @staticmethod
    async def create(user_configuration: UserConfigurationModel) -> UserConfigurationModel:
        return await user_configuration.create()

    @staticmethod
    async def update(user_configuration: UserConfigurationModel, **kwargs) -> UserConfigurationModel:
        return await user_configuration.update(asset=kwargs.get('asset', user_configuration.asset),
                                               fiat=kwargs.get('fiat', user_configuration.fiat),
                                               deposit=kwargs.get('deposit', user_configuration.deposit),
                                               spread_to=kwargs.get('spread_to', user_configuration.spread_to),
                                               spread_from=kwargs.get('spread_from', user_configuration.spread_from),
                                               exchange_buy=kwargs.get('exchange_buy', user_configuration.exchange_buy),
                                               trade_type_sell=kwargs.get('trade_type_sell',
                                                                          user_configuration.trade_type_sell),
                                               trade_type_buy=kwargs.get('trade_type_buy',
                                                                         user_configuration.trade_type_buy),
                                               payment_sell=kwargs.get('payment_sell', user_configuration.payment_sell),
                                               payment_buy=kwargs.get('payment_buy',
                                                                      user_configuration.payment_buy)).apply()

    @staticmethod
    async def get_by_tg_id(tg_id: int) -> UserConfigurationModel:
        user = await UserModel.query.where(UserModel.telegram_id == tg_id).gino.first()

        result = await UserConfigurationModel.query \
            .where(UserConfigurationModel.user_id == user.id) \
            .gino.first()
        return result

    @staticmethod
    async def get_by_id(id) -> Optional[UserConfigurationModel]:
        return await UserConfigurationModel.get(id)
