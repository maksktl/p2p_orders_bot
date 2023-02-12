import logging
from typing import Optional
from uuid import UUID

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from tgbot.services.dto import UserDto
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
        data['user'] = user
        data['config_active'] = await self.is_config_active(user.id)

    async def on_pre_process_callback_query(self, call: types.CallbackQuery, data: dict, *arg, **kwargs):
        try:
            user = await self.__user_service.get_user_by_tg_id(call.message.from_user.id)

        except Exception as err:
            logger.info(f'New user {call.message.from_user=}')
            user_dto = UserDto()
            user_dto.fill_from_user(call.message.from_user)
            user = await self.__user_service.create_user(user_dto)

        data['user'] = user

    async def is_config_active(self, user_id: UUID) -> Optional[bool]:
        try:
            user_config = await self.__user_configuration_service.get_user_conf_by_user_id(user_id)
            if user_config is not None and not user_config.deleted:
                return True
        except Exception as err:
            return None
        if user_config is None:
            return None
        return False
