import asyncio
import logging
from typing import List

from aiohttp import web
from sqlalchemy import and_

from tgbot.config import load_config
from tgbot.persistance import setup, shutdown
from tgbot.persistance.models import OrderModel

logger = logging.getLogger(__name__)


class WebApp:
    def __init__(self, port):
        self.port = port
        self.app = web.Application()
        self.app.add_routes([web.get('/get_banks', self.get_banks)])

    async def get_banks(self, request):
        exchange = request.query.get('exchange', '')
        fiat = request.query.get('fiat', '')

        orders: List[OrderModel] = await OrderModel.query.where(
            and_(OrderModel.asset == exchange, OrderModel.fiat == fiat, OrderModel.deleted == False)).gino.all()

        response_data = []
        for order in orders:
            response_data.extend(order.pay_type)
        return web.json_response(response_data)

    async def start_server(self):
        logger.info(f'Started server at port {self.port}')
        web.run_app(self.app, port=self.port)


async def main():
    try:
        config = load_config()
        web_app = WebApp(config.webapp_port)
        await setup(f'postgresql+asyncpg://{config.db.user}:{config.db.password}@{config.db.host}/{config.db.database}')
        runner = web.AppRunner(web_app.app)
        await runner.setup()
        site = web.TCPSite(runner, '0.0.0.0', web_app.port)
        await site.start()
        while True:
            await asyncio.sleep(1)
    finally:
        await shutdown()


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
        filename='server.log'
    )
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()
