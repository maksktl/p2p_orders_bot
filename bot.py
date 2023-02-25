import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from tgbot.config import load_config
from tgbot.filters.access_filter import BotAccessFilter
from tgbot.filters.admin_filter import IsAdminFilter
from tgbot.handlers.admin_hander import AdminHandler
from tgbot.handlers.p2p_handler import P2PHandler
from tgbot.handlers.user_handler import UserHandler
from tgbot.middlewares.acl_middleware import ACLMiddleware
from tgbot.middlewares.environment_middleware import EnvironmentMiddleware
from tgbot.persistance import setup, shutdown
from tgbot.services.notificator import Notificator
from tgbot.utils.scheduler_manager import SchedulerManager

logger = logging.getLogger(__name__)
handlers = []


def register_all_middlewares(dp, config):
    dp.setup_middleware(EnvironmentMiddleware(config=config))
    dp.setup_middleware(ACLMiddleware())


def register_all_filters(dp):
    dp.filters_factory.bind(IsAdminFilter)
    dp.filters_factory.bind(BotAccessFilter)


def register_all_handlers(dp):
    handlers.append(AdminHandler(dp))
    handlers.append(UserHandler(dp))
    handlers.append(P2PHandler(dp))


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
        # filename='tgbot.log'
    )
    logger.info("Starting bot")
    config = load_config(".env")

    storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)
    SchedulerManager().start()
    Notificator.get_instance(bot)

    bot['config'] = config

    register_all_middlewares(dp, config)
    register_all_filters(dp)
    register_all_handlers(dp)

    await setup(
        f'postgresql+asyncpg://{config.db.user}:{config.db.password}@{config.db.host}/{config.db.database}?client_encoding=utf8')
    try:
        await dp.start_polling()
    finally:
        await SchedulerManager().shutdown()
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()
        await shutdown()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
