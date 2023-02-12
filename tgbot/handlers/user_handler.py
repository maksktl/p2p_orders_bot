from aiogram import Dispatcher
from aiogram.types import Message, ReplyKeyboardMarkup

from tgbot.config import Config
from tgbot.handlers.base import BaseHandler
from tgbot.keyboards.reply import ReplyKeyboard


class UserHandler(BaseHandler):
    def __init__(self, dp: Dispatcher):
        super().__init__(dp)

    @staticmethod
    async def user_start(message: Message, config: Config, config_active):
        await message.answer(
            f"Приветствую, {message.chat.first_name}!\nНастрой свой поиск связки нажав на кнопку ниже.",
            reply_markup=ReplyKeyboard.get_web_app_conf_keyboard(config.tg_bot.webapp_url, config_active)
            )

    def register_methods(self):
        self.dp.register_message_handler(UserHandler.user_start, commands=["start"], state="*")
