import asyncio
import logging

from aiohttp import web
from sqlalchemy.sql import text

from tgbot.config import load_config
from tgbot.persistance import setup, shutdown, db
from tgbot.persistance.models import OrderModel

logger = logging.getLogger(__name__)


class WebApp:
    def __init__(self, port):
        self.port = port
        self.app = web.Application()
        self.app.add_routes([web.get('/banks', self.get_banks)])

    async def get_banks(self, request):
        sources = ''
        exchanges = request.query.get('exchanges', '').split(',')
        fiat = request.query.get('fiat', '')
        if exchanges:
            sources = 'AND (source = ANY(\'{"' + '", "'.join(exchanges) + '"}\'))'

        query = text(
            "SELECT r.pay_type FROM (SELECT unnest(pay_type) AS pay_type, COUNT(DISTINCT id) AS amount " +
            "FROM stock_order " +
            "WHERE fiat = :fiat " +
            sources + " GROUP BY pay_type) AS r GROUP BY r.pay_type ORDER BY SUM(r.amount) DESC, pay_type"
        ).bindparams(fiat=fiat)
        result = await db.all(query)
        result = list(map(lambda x: x[0], result))
        result = list(filter(lambda x: x is not None, result))
        return web.json_response(result)

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
