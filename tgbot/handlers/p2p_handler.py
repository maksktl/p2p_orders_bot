import json

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hcode

from tgbot.handlers.base import BaseHandler
from tgbot.services.user_configuration_service import UserConfigurationService


class P2PHandler(BaseHandler):
    USER_CONFIGURATION_SERVICE = UserConfigurationService.get_instance()

    def __init__(self, dp: Dispatcher):
        super().__init__(dp)

    @staticmethod
    async def bot_echo(message: types.Message):
        text = [
            "Эхо без состояния.",
            "Сообщение:",
            message.text
        ]

        await message.answer('\n'.join(text))

    @staticmethod
    async def bot_echo_all(message: types.Message, state: FSMContext):
        state_name = await state.get_state()
        text = [
            f'Эхо в состоянии {hcode(state_name)}',
            'Содержание сообщения:',
            hcode(message.text)
        ]
        await message.answer('\n'.join(text))
        await message.answer(message.web_app_data.data)

    @staticmethod
    async def apply_configuration(message: types.Message, *args, **kwargs):
        web_app_data = json.loads(message.web_app_data.data)
        await P2PHandler.USER_CONFIGURATION_SERVICE.create_or_update(web_app_data, message.from_user.id)

        await message.answer('☑️ Успешно применили новую конфигурацию для поиска связок')

    def register_methods(self):
        self.dp.register_message_handler(P2PHandler.bot_echo)
        self.dp.register_message_handler(P2PHandler.apply_configuration, state="*",
                                         content_types=types.ContentTypes.WEB_APP_DATA)
        self.dp.register_message_handler(P2PHandler.bot_echo_all, state="*", content_types=types.ContentTypes.ANY)
