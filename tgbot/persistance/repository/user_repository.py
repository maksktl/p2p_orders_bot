from typing import Optional

from sqlalchemy import text, bindparam, String, Float

from tgbot.persistance.models import UserModel


class UserRepository:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = UserRepository()
        return cls._instance

    @staticmethod
    async def create(user: UserModel):
        return await user.create()

    @staticmethod
    async def update(user: UserModel):
        return user.apply()

    @staticmethod
    async def get_by_id(id) -> Optional[UserModel]:
        return await UserModel.get(id)

    @staticmethod
    async def get_by_tg_id_and_deleted_false(tg_id):
        result = await UserModel.query.where((UserModel.telegram_id == tg_id) &
                                             (UserModel.deleted == False)).gino.first()
        return result
