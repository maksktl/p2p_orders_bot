from aiogram import Dispatcher
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.web_app_info import WebAppInfo

from tgbot.config import Config
from tgbot.handlers.base import BaseHandler


class UserHandler(BaseHandler):
    def __init__(self, dp: Dispatcher):
        super().__init__(dp)

    @staticmethod
    async def user_start(message: Message, config: Config):
        await message.answer("Hi", reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Конфигурация", web_app=WebAppInfo(url=config.tg_bot.webapp_url)), ]
            ]
        ))

    def register_methods(self):
        self.dp.register_message_handler(UserHandler.user_start, commands=["start"], state="*")
