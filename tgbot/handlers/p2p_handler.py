import json

from aiogram import types, Dispatcher

from tgbot.config import Config
from tgbot.handlers.base import BaseHandler
from tgbot.keyboards.reply import ReplyKeyboard
from tgbot.services.RestService import RestService
from tgbot.services.dto import UserFullDto
from tgbot.services.dto.user_configuration_dto import UserConfigurationDto


class P2PHandler(BaseHandler):
    REST_SERVICE = RestService.get_instance()

    def __init__(self, dp: Dispatcher):
        self._general_filters = {"bot_access": True}
        super().__init__(dp)

    @staticmethod
    async def apply_configuration(message: types.Message, config, user: UserFullDto):
        web_app_data = json.loads(message.web_app_data.data)
        dto = UserConfigurationDto(web_app_data)
        dto.userId = user.id

        await P2PHandler.REST_SERVICE.save_user_configuration(dto)

        await message.answer('☑️ Успешно применили новую конфигурацию для поиска связок',
                             reply_markup=ReplyKeyboard.get_web_app_conf_keyboard(config.tg_bot.webapp_url,
                                                                                  True))

    @staticmethod
    async def disable_configuration(message: types.Message, user: UserFullDto, config: Config, config_active):
        await P2PHandler.REST_SERVICE.disable_user_configuration(user.id)
        await message.answer('Поиск связок успешно отключен',
                             reply_markup=ReplyKeyboard.get_web_app_conf_keyboard(config.tg_bot.webapp_url,
                                                                                  config_active if not config_active
                                                                                  else not config_active))

    @staticmethod
    async def enable_configuration(message: types.Message, user: UserFullDto, config: Config, config_active):
        await P2PHandler.REST_SERVICE.enable_user_configuration(user.id)
        await message.answer('Поиск связок успешно активирован',
                             reply_markup=ReplyKeyboard.get_web_app_conf_keyboard(config.tg_bot.webapp_url,
                                                                                  not config_active))

    def register_methods(self):
        self.dp.register_message_handler(P2PHandler.apply_configuration, state="*",
                                         content_types=types.ContentTypes.WEB_APP_DATA, **self._general_filters)
        self.dp.register_message_handler(P2PHandler.disable_configuration, state="*", text='❌ Отключить поиск связок',
                                         **self._general_filters)
        self.dp.register_message_handler(P2PHandler.enable_configuration, state="*", text='✅ Включить поиск связок',
                                         **self._general_filters)
