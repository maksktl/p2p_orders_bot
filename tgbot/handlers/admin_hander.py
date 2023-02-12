from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.handlers.base import BaseHandler


class AdminHandler(BaseHandler):
    def __init__(self, dp: Dispatcher):
        super().__init__(dp)

    @staticmethod
    async def admin_start(message: Message):
        await message.reply("Hello, admin!")

    def register_methods(self):
        self.dp.register_message_handler(AdminHandler.admin_start, commands=["start"], state="*", is_admin=True)
