import logging

from gino import Gino
from gino.schema import GinoSchemaVisitor

db = Gino()
logger = logging.getLogger(__name__)


async def shutdown():
    bind = db.pop_bind()
    if bind:
        logger.info("Close PostgreSQL Connection")
        await bind.close()


async def setup(uri):
    logger.info("Setup PostgreSQL connection")
    logging.getLogger('gino.engine._SAEngine').setLevel(logging.ERROR)
    await db.set_bind(uri)

    # Create tables
    db.gino: GinoSchemaVisitor
    # await db.gino.drop_all()  # Drop the db
    await db.gino.create_all()
    logger.info('Database tables created')
