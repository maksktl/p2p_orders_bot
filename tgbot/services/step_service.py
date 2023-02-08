import asyncio
import logging
from typing import List

from tgbot.persistance.repository.step_repository import StepRepository
from tgbot.services.dto.step_full_dto import StepFullDto

logger = logging.getLogger(__name__)


class StepService:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = StepService()
        return cls._instance

    def __init__(self):
        self.__step_repository: StepRepository = StepRepository.get_instance()

    async def get_steps_by_user_id(self, user_id: int) -> List[StepFullDto]:
        steps = await self.__step_repository.get_steps_by_user(user_id)
        return [StepFullDto(step) for step in steps]

    async def get_steps_by_user_id_then_delete(self, user_id: int) -> List[StepFullDto]:
        steps = await self.__step_repository.get_steps_by_user(user_id)
        tasks = []
        for step in steps:
            tasks.append(asyncio.create_task(self.__step_repository.delete(step)))
        await asyncio.gather(*tasks)
        return [StepFullDto(step) for step in steps]
