import typing

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from tgbot.services.RestService import RestService


class BotAccessFilter(BoundFilter):
    key = 'bot_access'

    def __init__(self, bot_access: typing.Optional[bool] = None):
        self.bot_access = bot_access

    async def check(self, message: types.Message):
        user = await RestService.get_instance().current_user(message.from_user)
        return user.bot_access == self.bot_access
