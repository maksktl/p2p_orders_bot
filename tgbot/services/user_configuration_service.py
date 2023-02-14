import logging
from typing import List
from uuid import UUID

from tgbot.persistance.models import UserConfigurationModel
from tgbot.persistance.repository import UserRepository
from tgbot.persistance.repository.user_configuration_repository import UserConfigurationRepository
from tgbot.services.dto.user_configuration_dto import UserConfigurationDto
from tgbot.services.dto.user_configuration_full_dto import UserConfigurationFullDto

logger = logging.getLogger(__name__)


class UserConfigurationService:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = UserConfigurationService()
        return cls._instance

    def __init__(self):
        self.__user_configuration_repository = UserConfigurationRepository.get_instance()
        self.__user_repository = UserRepository.get_instance()

    async def get_user_conf(self, id) -> UserConfigurationFullDto:
        user_model = await self.__user_configuration_repository.get_by_id(id)
        if not user_model:
            raise Exception("User configuration not found")
        return UserConfigurationFullDto(user_model)

    async def get_user_conf_by_user_id(self, id: UUID) -> UserConfigurationFullDto:
        user_config = await self.__user_configuration_repository.get_by_user_id(id)
        if not user_config:
            raise Exception("User configuration not found")
        return UserConfigurationFullDto(user_config)

    async def create_user_conf(self, dto: UserConfigurationDto, user_id: int) -> UserConfigurationFullDto:
        user = await self.__user_repository.get_by_tg_id_and_deleted_false(user_id)
        if not user:
            raise Exception("User not found")
        dto.user_internal_id = user.id

        last_configuration = await self.__user_configuration_repository.get_by_tg_id(user_id)
        if not last_configuration:
            user_conf = UserConfigurationModel()
            user_conf.fill(dto)
            return UserConfigurationFullDto(await self.__user_configuration_repository.create(user_conf))
        else:
            raise Exception('Configuration already exists')

    async def create_or_update(self, payload: dict, user_id: int):
        dto = UserConfigurationDto(payload)
        user = await self.__user_repository.get_by_tg_id_and_deleted_false(user_id)
        if not user:
            raise Exception("User not found")
        dto.user_internal_id = user.id

        configuration = await self.__user_configuration_repository.get_by_tg_id(user_id)
        if not configuration:
            user_conf = UserConfigurationModel()
            user_conf.fill(dto)
            await self.__user_configuration_repository.create(user_conf)
            return

        return await self.__user_configuration_repository.update(configuration, **dto.__dict__)

    async def get_all_active(self) -> List[UserConfigurationFullDto]:
        configurations = await self.__user_configuration_repository.get_all_by_deleted_false()
        return [UserConfigurationFullDto(configuration) for configuration in
                configurations]

    async def disable_configuration(self, user_id: UUID):
        return await self.__user_configuration_repository.delete_by_user_id(user_id) is not None

    async def enable_configuration(self, user_id: UUID):
        return await self.__user_configuration_repository.restore_by_user_id(user_id) is not None
