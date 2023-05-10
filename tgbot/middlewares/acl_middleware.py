import logging

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from tgbot.services.RestService import RestService

logger = logging.getLogger(__name__)


class ACLMiddleware(BaseMiddleware):
    def __init__(self):
        super().__init__()
        self.__rest_service = RestService().get_instance()

    async def on_pre_process_message(self, message: types.Message, data: dict, *args, **kwargs):
        user = await self.__rest_service.current_user(message.from_user)
        data['user'] = user
        data['user_configuration'] = await self.__rest_service.get_user_configuration(user.id)
        data['config_active'] = not data.get('user_configuration').deleted if data.get(
            'user_configuration') is not None else None
        if data.get('user_configuration') is not None:
            data['user_configuration'].user = user

    async def on_pre_process_callback_query(self, call: types.CallbackQuery, data: dict, *arg, **kwargs):
        user = await self.__rest_service.current_user(call.from_user)
        data['user'] = user
        data['user_configuration'] = await self.__rest_service.get_user_configuration(user.id)
        data['config_active'] = not data.get('user_configuration').deleted if data.get(
            'user_configuration') is not None else None
        if data.get('user_configuration') is not None:
            data['user_configuration'].user = user
