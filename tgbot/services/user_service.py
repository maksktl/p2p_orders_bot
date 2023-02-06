import logging

from tgbot.persistance.models import UserModel
from tgbot.persistance.repository import UserRepository
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

    def get_user(self, id) -> UserFullDto:
        user_model = await self.__user_repository.get_by_id(id)
        if not user_model:
            raise Exception("User not found")
        return UserFullDto(user_model)

    def get_user_by_tg_id(self, tg_id) -> UserFullDto:
        user_model = await self.__user_repository.get_by_tg_id_and_deleted_false(tg_id)
        if not user_model:
            raise Exception("User not found")
        return UserFullDto(user_model)

    def create_user(self, user_dto: UserDto) -> UserFullDto:
        if user_dto.telegram_id and await self.__user_repository.get_by_tg_id_and_deleted_false(
                user_dto.telegram_id):
            raise Exception("User already exists")
        user_model = UserModel(user_dto)
        return UserFullDto(await self.__user_repository.create(user_model))

    def update_user(self, user_dto: UserDto):
        user_model = await self.__user_repository.get_by_id(user_dto.id)
        if not user_model:
            user_model = await self.__user_repository.get_by_tg_id_and_deleted_false(user_dto.telegram_id)
        if not user_model:
            raise Exception("User not found")
        return UserFullDto(await self.__user_repository.update(user_model.update(user_dto)))