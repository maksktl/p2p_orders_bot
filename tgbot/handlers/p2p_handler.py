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
    async def disable_configuration(message: types.Message, config, user, config_active, *args, **kwargs):
        if not config_active:
            await message.answer('Поиск связок уже был отключен',
                                 reply_markup=ReplyKeyboard.get_web_app_conf_keyboard(config.tg_bot.webapp_url,
                                                                                      config_active))
            return
        is_disabled = await P2PHandler.USER_CONFIGURATION_SERVICE.disable_configuration(user.id)
        if is_disabled:
            await message.answer('Поиск связок успешно отключен',
                                 reply_markup=ReplyKeyboard.get_web_app_conf_keyboard(config.tg_bot.webapp_url, False))
            return
        await message.answer('Произошла ошибка, разработчики уже над ней работают :)',
                             reply_markup=ReplyKeyboard.get_web_app_conf_keyboard(config.tg_bot.webapp_url,
                                                                                  config_active))

    @staticmethod
    async def enable_configuration(message: types.Message, config, user, config_active, *args, **kwargs):
        if config_active:
            await message.answer('Поиск связок уже был активироан',
                                 reply_markup=ReplyKeyboard.get_web_app_conf_keyboard(config.tg_bot.webapp_url,
                                                                                      config_active))
            return
        is_active = await P2PHandler.USER_CONFIGURATION_SERVICE.enable_configuration(user.id)
        if is_active:
            await message.answer('Поиск связок успешно активирован',
                                 reply_markup=ReplyKeyboard.get_web_app_conf_keyboard(config.tg_bot.webapp_url, True))
            return
        await message.answer('Произошла ошибка, разработчики уже над ней работают :)',
                             reply_markup=ReplyKeyboard.get_web_app_conf_keyboard(config.tg_bot.webapp_url,
                                                                                  config_active))

    def register_methods(self):
        self.dp.register_message_handler(P2PHandler.apply_configuration, state="*",
                                         content_types=types.ContentTypes.WEB_APP_DATA)
        self.dp.register_message_handler(P2PHandler.disable_configuration, state="*", text='❌ Отключить поиск связок')
        self.dp.register_message_handler(P2PHandler.enable_configuration, state="*", text='✅ Включить поиск связок')
