import logging
from typing import Optional
from uuid import UUID

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from tgbot.services.dto import UserDto
from tgbot.services.dto.user_configuration_full_dto import UserConfigurationFullDto
from tgbot.services.user_configuration_service import UserConfigurationService
from tgbot.services.user_service import UserService

logger = logging.getLogger(__name__)


class ACLMiddleware(BaseMiddleware):
    def __init__(self):
        super().__init__()
        self.__user_service = UserService.get_instance()
        self.__user_configuration_service = UserConfigurationService.get_instance()

    async def on_pre_process_message(self, message: types.Message, data: dict, *args, **kwargs):
        try:
            user = await self.__user_service.get_user_by_tg_id(message.from_user.id)

        except Exception as err:
            logger.info(f'New user {message.from_user=}')
            user_dto = UserDto()
            user_dto.fill_from_user(message.from_user)
            user = await self.__user_service.create_user(user_dto)
        if user.name != message.from_user.first_name or user.name == 'Not Authorized':
            user_dto = UserDto()
            user_dto.fill_from_user(message.from_user)
            user = await self.__user_service.update_user(user_dto)
        data['user'] = user
        data['user_configuration'] = await self.get_user_configuration(user.id)
        data['config_active'] = not data.get('user_configuration').deleted if data.get(
            'user_configuration') is not None else None

    async def on_pre_process_callback_query(self, call: types.CallbackQuery, data: dict, *arg, **kwargs):
        try:
            user = await self.__user_service.get_user_by_tg_id(call.message.from_user.id)

        except Exception as err:
            logger.info(f'New user {call.message.from_user=}')
            user_dto = UserDto()
            user_dto.fill_from_user(call.message.from_user)
            user = await self.__user_service.create_user(user_dto)

        data['user'] = user

    async def get_user_configuration(self, user_id: UUID) -> Optional[UserConfigurationFullDto]:
        try:
            user_config = await self.__user_configuration_service.get_user_conf_by_user_id(user_id)
            if user_config is not None and not user_config.deleted:
                return user_config
        except Exception as err:
            return None
        return None
