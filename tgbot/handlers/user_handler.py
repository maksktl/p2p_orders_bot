from aiogram import Dispatcher
from aiogram.types import Message, ReplyKeyboardRemove

from tgbot.config import Config
from tgbot.handlers.base import BaseHandler
from tgbot.keyboards.reply import ReplyKeyboard
from tgbot.services.dto.user_configuration_full_dto import UserConfigurationFullDto


class UserHandler(BaseHandler):
    def __init__(self, dp: Dispatcher):
        self._general_filters = {"bot_access": True}
        super().__init__(dp)

    @staticmethod
    async def user_start(message: Message, config: Config, config_active):
        await message.answer(
            f"Приветствую, {message.chat.first_name}!\nНастрой свой поиск связки нажав на кнопку ниже.",
            reply_markup=ReplyKeyboard.get_web_app_conf_keyboard(config.tg_bot.webapp_url, config_active)
        )

    @staticmethod
    async def user_not_accessed(message: Message):
        await message.answer(
            f"Приветствую, {message.chat.first_name}!\n"
            f"Чтобы получить доступ к боту отправь код <code>{message.from_user.id}</code> <a href=\"tg://user?id=254727353\">Менеджеру</a>",
            reply_markup=ReplyKeyboardRemove()
        )

    async def user_lk(self, message: Message, user_configuration: UserConfigurationFullDto):
        config_text = '❌ Поиск связок не настроен'
        if user_configuration:
            config_text = f'Параметры вашей конфигурации:\n' \
                          f'Фиат: {user_configuration.fiat}\n' \
                          f'Выбранные криптовалюты: {",".join(user_configuration.asset)}\n' \
                          f'\n' \
                          f'Установленный лимит: {user_configuration.deposit / 100.0}\n' \
                          f'Установленный диапозон спреда: {user_configuration.spread_from / 100.0}' \
                          f' - {user_configuration.spread_to / 100.0}\n' \
                          f'\n' \
                          f'<bold>Покупка</bold>\n' \
                          f'Выбранные биржи: {",".join(user_configuration.exchange_buy)}\n' \
                          f'Выбранные способы оплаты: {",".join(user_configuration.payment_buy)}\n' \
                          f'Покупаете как: {user_configuration.trade_type_buy}\n' \
                          f'\n'\
                          f'<bold>Продажа</bold>\n' \
                          f'Выбранные биржи: {",".join(user_configuration.exchange_sell)}\n' \
                          f'Выбранные способы оплаты: {",".join(user_configuration.payment_sell)}\n' \
                          f'Продаете как: {user_configuration.trade_type_sell}'
        await message.answer(f'Профиль: 📜\n'
                             f'ID: <code>{message.from_user.id}</code>\n'
                             f'\n'
                             f'Имя: {message.from_user.first_name}\n'
                             f'\n'+config_text)

    def register_methods(self):
        self.dp.register_message_handler(UserHandler.user_start, commands=["start"], state="*", **self._general_filters)
        self.dp.register_message_handler(UserHandler.user_lk(), commands=["lk"], state="*", **self._general_filters)
        self.dp.register_message_handler(UserHandler.user_not_accessed, bot_access=False)
