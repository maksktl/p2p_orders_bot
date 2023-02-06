import json

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hcode

from tgbot.handlers.base import BaseHandler


class TestHandler(BaseHandler):

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

    def register_methods(self):
        self.dp.register_message_handler(TestHandler.bot_echo)
        self.dp.register_message_handler(TestHandler.bot_echo_all, state="*", content_types=types.ContentTypes.ANY)
