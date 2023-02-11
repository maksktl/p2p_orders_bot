import asyncio
from typing import List, Union
from uuid import UUID

from sqlalchemy import or_, and_

from tgbot.persistance.models import StepModel


class StepRepository:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = StepRepository()
        return cls._instance

    @staticmethod
    async def create(step: StepModel) -> StepModel:
        return await step.create()

    @staticmethod
    async def get_steps_by_user(user_id: UUID) -> List[StepModel]:
        return await StepModel.query.where(
            StepModel.user_id == user_id,
            StepModel.deleted == False
        ).gino.all()

    @staticmethod
    async def get_step_by_user_id_and_order_buy_id_and_order_sell_id(user_id, order_buy_id, order_sell_id) -> Union[
        StepModel, None]:
        return await StepModel.query.where(
            and_(StepModel.user_id == user_id,
                 StepModel.order_buy_id == order_buy_id, StepModel.order_sell_id == order_sell_id)
        ).gino.first()

    @staticmethod
    async def delete(step: StepModel) -> StepModel:
        query = StepModel.update.values(
            deleted=True
        ).where(
            or_(
                StepModel.user_id == step.user_id,
                StepModel.id == step.id
            )
        )
        return await query.gino.status()

    @staticmethod
    async def save_all(steps: List[StepModel]):
        tasks = [asyncio.create_task(step.create()) for step in steps]
        await asyncio.gather(*tasks)
