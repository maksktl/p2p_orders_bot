import logging
from typing import List

from tgbot.persistance.repository.order_repository import OrderRepository
from tgbot.services.dto.order_full_dto import OrderFullDto

logger = logging.getLogger(__name__)


class OrderService:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = OrderService()
        return cls._instance

    def __init__(self):
        self.__order_repository = OrderRepository

    async def get(self, id) -> OrderFullDto:
        order_model = await self.__order_repository.get_by_id(id)
        if not order_model:
            raise Exception("Order not found")
        return OrderFullDto(order_model)

    async def get_all(self) -> List[OrderFullDto]:
        orders = await self.__order_repository.get_all()
        return [OrderFullDto(order) for order in orders]

    @staticmethod
    async def calculate_spread(sell_price, buy_price) -> float:
        return (sell_price / buy_price) * 100 - 100
