import typing

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from tgbot.services.user_service import UserService


class IsAdminFilter(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin: typing.Optional[bool] = None):
        self.is_admin = is_admin

    async def check(self, message: types.Message):
        user = await UserService.get_instance().get_user_by_tg_id(message.from_user.id)
        return user.admin == self.is_admin
