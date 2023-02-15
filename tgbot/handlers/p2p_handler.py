import json

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hcode

from tgbot.handlers.base import BaseHandler
from tgbot.keyboards.reply import ReplyKeyboard
from tgbot.services.user_configuration_service import UserConfigurationService


class P2PHandler(BaseHandler):
    USER_CONFIGURATION_SERVICE = UserConfigurationService.get_instance()

    def __init__(self, dp: Dispatcher):
        super().__init__(dp)

    @staticmethod
    async def apply_configuration(message: types.Message, config, config_active, *args, **kwargs):
        web_app_data = json.loads(message.web_app_data.data)
        await P2PHandler.USER_CONFIGURATION_SERVICE.create_or_update(web_app_data, message.from_user.id)

        await message.answer('☑️ Успешно применили новую конфигурацию для поиска связок',
                             reply_markup=ReplyKeyboard.get_web_app_conf_keyboard(config.tg_bot.webapp_url,
                                                                                  config_active))

    @staticmethod
    async def handle_configuration(message: types.Message, config, user, config_active, enabled: bool,
                                   success_text: str):
        if enabled == config_active:
            await message.answer(f'Поиск связок уже {"был активирован" if enabled else "был отключен"}',
                                 reply_markup=ReplyKeyboard.get_web_app_conf_keyboard(config.tg_bot.webapp_url,
                                                                                      config_active))
            return
        is_enabled = await P2PHandler.USER_CONFIGURATION_SERVICE.enable_configuration(
            user.id) if enabled else await P2PHandler.USER_CONFIGURATION_SERVICE.disable_configuration(user.id)
        if is_enabled:
            await message.answer(success_text,
                                 reply_markup=ReplyKeyboard.get_web_app_conf_keyboard(config.tg_bot.webapp_url,
                                                                                      enabled))
            return
        await message.answer('Произошла ошибка, разработчики уже над ней работают :)',
                             reply_markup=ReplyKeyboard.get_web_app_conf_keyboard(config.tg_bot.webapp_url,
                                                                                  config_active))

    @staticmethod
    async def disable_configuration(message: types.Message, config, user, config_active, *args, **kwargs):
        await P2PHandler.handle_configuration(message, config, user, config_active, False,
                                              'Поиск связок успешно отключен')

    @staticmethod
    async def enable_configuration(message: types.Message, config, user, config_active, *args, **kwargs):
        await P2PHandler.handle_configuration(message, config, user, config_active, True,
                                              'Поиск связок успешно активирован')

    def register_methods(self):
        self.dp.register_message_handler(P2PHandler.apply_configuration, state="*",
                                         content_types=types.ContentTypes.WEB_APP_DATA)
        self.dp.register_message_handler(P2PHandler.disable_configuration, state="*", text='❌ Отключить поиск связок')
        self.dp.register_message_handler(P2PHandler.enable_configuration, state="*", text='✅ Включить поиск связок')