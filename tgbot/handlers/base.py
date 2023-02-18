from aiogram import Dispatcher


class BaseHandler:
    def __init__(self, dp: Dispatcher):
        self.dp = dp
        self.register_methods()

    def register_methods(self):
        raise NotImplementedError
