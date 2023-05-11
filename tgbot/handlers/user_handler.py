from aiogram import Dispatcher
from aiogram.types import Message, ReplyKeyboardRemove, LabeledPrice, PreCheckoutQuery

from tgbot.config import Config
from tgbot.handlers.base import BaseHandler
from tgbot.keyboards.reply import ReplyKeyboard
from tgbot.misc.Item import Item
from tgbot.services.RestService import RestService
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
    async def user_not_accessed(message: Message, config: Config):
        await message.answer(
            f'Привет от команды Crypto-Max. \n'
            f'Для того чтобы активировать бота нужно оформить подписку',
            reply_markup=ReplyKeyboardRemove()
        )
        item = Item(
            title="Доступ к боту",
            description="Доступ к боту на месяц",
            currency="RUB",
            prices=[
                LabeledPrice(
                    label="Доступ к боту",
                    amount=1000_00
                )
            ],
            start_parameter="create_invoice",
            photo_url="https://i.ibb.co/vXcNK2K/Color-logo-with-background.png",
            provider_token=config.provider_token
        )

        await message.bot.send_invoice(message.chat.id, **item.generate_invoice(), payload="1")

    @staticmethod
    async def process_pre_checkout_query(query: PreCheckoutQuery):
        await query.bot.answer_pre_checkout_query(pre_checkout_query_id=query.id, ok=True)
        user = await RestService.get_instance().get_user_by_telegram_id(query.from_user.id)
        await RestService.get_instance().grant_access_user(user.id, 1)
        await query.bot.send_message(chat_id=query.from_user.id, text="Спасибо за покупку! \n"
                                                                      "Теперь вы имеете полный доступ к боту!"
                                                                      "\n"
                                                                      "Нажмите /start для начала пользования.")

    @staticmethod
    async def user_lk(message: Message, config, user_configuration: UserConfigurationFullDto, config_active):
        config_text = '❌ Поиск связок: не настроен'
        if user_configuration:
            config_text = f'<b>Параметры вашей конфигурации:</b>\n' \
                          f'<b>Фиат: 💰</b> {user_configuration.fiat}\n' \
                          f'<b>Выбранные криптовалюты: 💎</b> {", ".join(user_configuration.asset)}\n' \
                          f'\n' \
                          f'<b>Установленный лимит: 📛</b> {user_configuration.deposit / 100.0}\n' \
                          f'<b>Установленный диапозон спреда: ↔️</b> {user_configuration.spread_from / 100.0}' \
                          f' - {user_configuration.spread_to / 100.0}\n' \
                          f'\n' \
                          f'<b>Покупка 📉</b>\n' \
                          f'<b>Выбранные биржи: 📊</b> {", ".join(user_configuration.exchange_buy)}\n' \
                          f'<b>Выбранные способы оплаты: 💳</b> {", ".join(user_configuration.payment_buy)}\n' \
                          f'<b>Покупаете как: 👤</b> {user_configuration.trade_type_buy}\n' \
                          f'\n' \
                          f'<b>Продажа 📈</b>\n' \
                          f'<b>Выбранные биржи: 📊</b> {", ".join(user_configuration.exchange_sell)}\n' \
                          f'<b>Выбранные способы оплаты: 💳</b> {", ".join(user_configuration.payment_sell)}\n' \
                          f'<b>Продаете как: 👤</b> {user_configuration.trade_type_sell}\n' \
                          f'\n' \
                          f'<b>Поиск связок: {"✅ Активен" if not user_configuration.deleted else "❌ Не активен"}</b>'
        await message.answer_photo(photo='https://i.ibb.co/vXcNK2K/Color-logo-with-background.png',
                                   caption=f'<b>Профиль:</b> 🧑🏽‍💻\n'
                                           f'<b>ID:</b> <code>{message.from_user.id}</code>\n'
                                           f'<b>Имя:</b> {message.from_user.first_name}\n'
                                           f'\n' + config_text,
                                   reply_markup=ReplyKeyboard.get_web_app_conf_keyboard(config.tg_bot.webapp_url,
                                                                                        config_active))

    @staticmethod
    async def default_message(message: Message):
        await message.answer('Вы можете использовать следующие команды:\n\n'
                             '/start - стартовое сообщение бота с конфигурацией свзяки\n'
                             '/lk - Данные вашего профиля в боте\n\n'
                             'По остальным вопросам пишите <a href=\"https://t.me/BatFlex\">Менеджеру</a>')

    def register_methods(self):
        self.dp.register_message_handler(UserHandler.user_start, commands=["start"], state="*", **self._general_filters)
        self.dp.register_message_handler(UserHandler.user_lk, commands=["lk"], state="*", **self._general_filters)
        self.dp.register_message_handler(UserHandler.user_not_accessed, bot_access=False)
        self.dp.register_message_handler(UserHandler.default_message, **self._general_filters)
        self.dp.register_pre_checkout_query_handler(UserHandler.process_pre_checkout_query)
