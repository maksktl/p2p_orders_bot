import asyncio
import logging
from typing import List
from uuid import UUID

from aiogram import Bot

from tgbot.services.dto.step_full_dto import StepFullDto
from tgbot.services.order_service import OrderService
from tgbot.services.step_service import StepService
from tgbot.services.user_configuration_service import UserConfigurationService

logger = logging.getLogger(__name__)


class Notificator:
    _instance = None
    _bot: Bot = None

    @classmethod
    def get_instance(cls, bot=None):
        if cls._instance is None:
            cls._instance = Notificator()
            cls._bot = bot
        return cls._instance

    def __init__(self):
        self.__step_service: StepService = StepService.get_instance()
        self.__user_configuration_service: UserConfigurationService = UserConfigurationService.get_instance()

    async def send_steps(self):
        configurations = await self.__user_configuration_service.get_all_active()
        await asyncio.gather(
            *[asyncio.create_task(self._send_steps(configuration.user_id, configuration.user.telegram_id)) for
              configuration in configurations])

    async def _send_steps(self, user_id: UUID, user_tg_id: int):
        steps = await self.__step_service.get_steps_by_user_id_then_delete(user_id)
        await self._send_steps_to_user(user_tg_id, steps)

    async def _send_steps_to_user(self, user_id: int, steps: List[StepFullDto]):
        text = f'🔥 Уведомление | Найдено новых связок - {len(steps)} \n\n'
        for step in steps:
            text = text + f'{step.order_buy.asset} [{step.order_buy.source}] {step.strategy_type_buy}' \
                          f' {step.order_buy.pay_type} {step.order_buy.price}' \
                          f' → ' \
                          f'{step.order_sell.asset} [{step.order_sell.source}] {step.strategy_type_sell}' \
                          f' {step.order_sell.pay_type} {step.order_sell.price} ' \
                          f'Spread: {OrderService.calculate_spread(step.order_sell.price, step.order_buy.price)}%\n'
        await self._bot.send_message(user_id, text)
