import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler


class SchedulerManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.scheduler = AsyncIOScheduler()
            logging.getLogger('apscheduler.scheduler').setLevel(logging.ERROR)
            logging.getLogger('apscheduler.executors.default').setLevel(logging.ERROR)
        return cls._instance

    def start(self):
        self.scheduler.start()

    def shutdown(self, wait=True):
        self.scheduler.shutdown(wait=wait)

    def add_job(self, func, trigger, *args, **kwargs):
        self.scheduler.add_job(func, trigger, *args, **kwargs)


def scheduled(trigger='interval', *args, **kwargs):
    def decorator(func):
        SchedulerManager().add_job(func, trigger, *args, **kwargs)
        return func

    return decorator


"""
scheduler = SchedulerManager()
scheduler.start()

@scheduled(trigger='interval', seconds=10)
async def my_async_job():
    print("Hello World")

scheduler.shutdown()
"""
