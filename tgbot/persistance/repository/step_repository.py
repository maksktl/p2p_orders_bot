from typing import List

from sqlalchemy import or_

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
    async def update(step: StepModel) -> StepModel:
        query = StepModel.update.values(
            next_step_id=step.next_step_id,
            deleted=step.deleted,
            order_id=step.order_id
        ).where(
            or_(
                StepModel.user_id == step.user_id,
                StepModel.id == step.id
            )
        )
        return await query.gino.status()

    @staticmethod
    async def get_steps_by_user(user_id) -> List[StepModel]:
        return await StepModel.query.where(
            StepModel.user_id == user_id,
            StepModel.deleted == False
        ).gino.all()

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
