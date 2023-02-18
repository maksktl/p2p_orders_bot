from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.handlers.base import BaseHandler


class AdminHandler(BaseHandler):
    def __init__(self, dp: Dispatcher):
        self._general_filters = {"bot_access": True, 'is_admin': True}
        super().__init__(dp)
        self._general_filters['is_admin'] = True

    @staticmethod
    async def admin_start(message: Message):
        await message.reply("Hello, admin!")

    def register_methods(self):
        self.dp.register_message_handler(AdminHandler.admin_start, commands=["start"], state="*",
                                         **self._general_filters)
