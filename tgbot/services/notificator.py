import asyncio
import logging
from typing import List
from uuid import UUID

from aiogram import Bot

from tgbot.services.RestService import RestService
from tgbot.services.dto.step_full_dto import StepFullDto
from tgbot.services.dto.user_configuration_full_dto import UserConfigurationFullDto
from tgbot.utils.scheduler_manager import scheduled

logger = logging.getLogger(__name__)


class Notificator:
    _instance = None
    BOT: Bot = None
    REST_SERVICE = RestService.get_instance()

    @classmethod
    def get_instance(cls, bot=None):
        if cls._instance is None:
            cls._instance = Notificator()
            Notificator.BOT = bot
        return cls._instance

    @staticmethod
    @scheduled(trigger='interval', seconds=10)
    async def send_steps():
        configurations = await Notificator.REST_SERVICE.get_all_user_configurations()
        await asyncio.gather(
            *[asyncio.create_task(Notificator._send_steps(configuration)) for
              configuration in configurations])

    @staticmethod
    async def _send_steps(user_configuration: UserConfigurationFullDto):
        steps = await Notificator.REST_SERVICE.get_user_steps(user_configuration.user_id)
        await Notificator._send_steps_to_user(user_configuration, steps)

    @staticmethod
    async def _send_steps_to_user(user_configuration: UserConfigurationFullDto, steps: List[StepFullDto]):
        if len(steps) == 0:
            return
        text = f'🔥 Уведомление | Найдено новых связок - {len(steps)} \n\n'
        messages = [text]
        for step in steps:
            text = messages[-1]
            new_text = f'<code>{step.order_buy.username}</code> {step.order_buy.asset} [{step.order_buy.source}] {step.strategy_type_buy.capitalize()}' \
                       f' {", ".join(step.order_buy.pay_type)} <code>{step.order_buy.price / 100}</code>' \
                       f' → ' \
                       f'<code>{step.order_sell.username}</code> {step.order_sell.asset} [{step.order_sell.source}] {step.strategy_type_sell.capitalize()}' \
                       f' {", ".join(step.order_sell.pay_type)} <code>{step.order_sell.price / 100}</code> ' \
                       f'Spread: {step.spread / 100}%\n\n'
            if len(text + new_text) > 4096:
                messages.append(text)
                messages.append(new_text)
            else:
                messages[-1] = text + new_text

        for message in messages:
            await Notificator.BOT.send_message(user_configuration.user.telegram_id, message, protect_content=True)
