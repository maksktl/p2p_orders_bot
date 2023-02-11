import asyncio
import logging
from typing import List
from uuid import UUID

from aiogram import Bot

from tgbot.services.dto.step_full_dto import StepFullDto
from tgbot.services.order_service import OrderService
from tgbot.services.step_service import StepService
from tgbot.services.user_configuration_service import UserConfigurationService
from tgbot.utils.scheduler_manager import scheduled

logger = logging.getLogger(__name__)


class Notificator:
    _instance = None
    BOT: Bot = None
    STEP_SERVICE: StepService = None
    USER_CONFIGURATION_SERVICE: UserConfigurationService = None

    @classmethod
    def get_instance(cls, bot=None):
        if cls._instance is None:
            cls._instance = Notificator()
            Notificator.BOT = bot
            Notificator.STEP_SERVICE: StepService = StepService.get_instance()
            Notificator.USER_CONFIGURATION_SERVICE: UserConfigurationService = UserConfigurationService.get_instance()
            Notificator.BOT = bot
        return cls._instance

    @staticmethod
    @scheduled(trigger='interval', seconds=10)
    async def send_steps():
        configurations = await Notificator.USER_CONFIGURATION_SERVICE.get_all_active()
        await asyncio.gather(
            *[asyncio.create_task(Notificator._send_steps(configuration.user_id, configuration.user.telegram_id)) for
              configuration in configurations])

    @staticmethod
    async def _send_steps(user_id: UUID, user_tg_id: int):
        steps = await Notificator.STEP_SERVICE.get_steps_by_user_id_then_delete(user_id)
        await Notificator._send_steps_to_user(user_tg_id, steps)

    @staticmethod
    async def _send_steps_to_user(user_id: int, steps: List[StepFullDto]):
        if len(steps) == 0:
            return
        text = f'🔥 Уведомление | Найдено новых связок - {len(steps)} \n\n'
        messages = [text]
        for step in steps:
            text = messages[-1]
            new_text = f'{step.order_buy.asset} [{step.order_buy.source}] {step.strategy_type_buy}' \
                       f' {", ".join(step.order_buy.pay_type)} {step.order_buy.price}' \
                       f' → ' \
                       f'{step.order_sell.asset} [{step.order_sell.source}] {step.strategy_type_sell}' \
                       f' {", ".join(step.order_sell.pay_type)} {step.order_sell.price} ' \
                       f'Spread: {await OrderService.calculate_spread(step.order_sell.price, step.order_buy.price)}%\n\n'
            if len(text+new_text) > 4096:
                messages.append(text)
                messages.append(new_text)
            else:
                messages[-1] = text + new_text

        for message in messages:
            await Notificator.BOT.send_message(user_id, message)
