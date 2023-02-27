import logging

from tgbot.persistance.models import UserModel
from tgbot.persistance.repository import UserRepository
from tgbot.persistance.repository.user_configuration_repository import UserConfigurationRepository
from tgbot.services.dto import UserFullDto, UserDto

logger = logging.getLogger(__name__)


class UserService:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = UserService()
        return cls._instance

    def __init__(self):
        self.__user_repository = UserRepository.get_instance()
        self.__user_configuration_repository = UserConfigurationRepository.get_instance()

    async def get_user(self, id) -> UserFullDto:
        user_model = await self.__user_repository.get_by_id(id)
        if not user_model:
            raise Exception("User not found")
        return UserFullDto(user_model)

    async def get_user_by_tg_id(self, tg_id) -> UserFullDto:
        user_model = await self.__user_repository.get_by_tg_id_and_deleted_false(tg_id)
        if not user_model:
            raise Exception("User not found")
        return UserFullDto(user_model)

    async def create_user(self, user_dto: UserDto) -> UserFullDto:
        if user_dto.telegram_id and await self.__user_repository.get_by_tg_id_and_deleted_false(
                user_dto.telegram_id):
            raise Exception("User already exists")
        user_model = UserModel()
        user_model.fill(user_dto)
        return UserFullDto(await self.__user_repository.create(user_model))

    async def update_user(self, user_dto: UserDto):
        user_model = await self.__user_repository.get_by_id(user_dto.id)
        if not user_model:
            user_model = await self.__user_repository.get_by_tg_id_and_deleted_false(user_dto.telegram_id)
        if not user_model:
            raise Exception("User not found")
        return UserFullDto(await self.__user_repository.update(user_model.update_by_dto(user_dto)))

    async def set_user_settings(self, tg_id, admin: bool = None, bot_access: bool = None):
        user_model = await self.__user_repository.get_by_tg_id_and_deleted_false(tg_id)
        if not user_model:
            user_model = UserModel()
            user_model.telegram_id = tg_id
            if admin is not None:
                user_model.admin = admin
            if bot_access is not None:
                user_model.bot_access = bot_access
            await self.__user_repository.create(user_model)
            return
        if admin is not None:
            user_model.admin = admin
        if bot_access is not None:
            user_model.bot_access = bot_access
            if not bot_access:
                user_model.admin = False
                self.__user_configuration_repository.delete_by_user_id(user_model.id)

        await self.__user_repository.update(user_model)
