from typing import Optional

from tgbot.persistance import db
from tgbot.persistance.models import UserConfigurationModel
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
    async def update(user_configuration: UserConfigurationModel) -> UserConfigurationModel:
        return await user_configuration.apply()

    @staticmethod
    async def get_by_tg_id(tg_id: int) -> UserConfigurationModel:
        query = text('SELECT uc.* FROM user_configuration AS uc '
                     'LEFT JOIN public.user AS u ON u.id = uc.user_id '
                     'WHERE u.telegram_id = :tg_id').bindparams(tg_id=tg_id)
        result = await db.first(query)
        return result

    @staticmethod
    async def get_by_id(id) -> Optional[UserConfigurationModel]:
        return await UserConfigurationModel.get(id)
