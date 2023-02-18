import typing

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from tgbot.services.user_service import UserService


class BotAccessFilter(BoundFilter):
    key = 'bot_access'

    def __init__(self, bot_access: typing.Optional[bool] = None):
        self.bot_access = bot_access

    async def check(self, message: types.Message):
        user = await UserService.get_instance().get_user_by_tg_id(message.from_user.id)
        return user.bot_access == self.bot_access
