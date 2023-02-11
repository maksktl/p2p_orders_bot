from typing import Optional

from tgbot.persistance.models.order_model import OrderModel


class OrderRepository:

    @staticmethod
    async def get_by_id(id) -> Optional[OrderModel]:
        return await OrderModel.get(id)

    @staticmethod
    async def get_by_external_id_and_deleted_false(external_id):
        result = await OrderModel.query.where((OrderModel.external_id == external_id) &
                                              (OrderModel.deleted == False)).gino.first()
        return result

    @staticmethod
    async def get_all_by_asset_and_deleted_false(asset):
        return await OrderModel.query.where((OrderModel.asset == asset) &
                                            (OrderModel.deleted == False)).gino.all()

    @staticmethod
    async def get_all_before_date(date):
        return await OrderModel.query.where((OrderModel.updated_at < date) & (OrderModel.deleted == False)).gino.all()

    @staticmethod
    async def get_all():
        return await OrderModel.query.where(OrderModel.deleted == False).gino.all()
