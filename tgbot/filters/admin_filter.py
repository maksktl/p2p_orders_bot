import typing

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from tgbot.services.RestService import RestService


class IsAdminFilter(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin: typing.Optional[bool] = None):
        self.is_admin = is_admin

    async def check(self, message: types.Message):
        user = await RestService.get_instance().current_user(message.from_user)
        return user.admin == self.is_admin
