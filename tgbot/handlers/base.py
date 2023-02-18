from aiogram import Dispatcher


class BaseHandler:
    _general_filters = {"bot_access": True}

    def __init__(self, dp: Dispatcher):
        self.dp = dp
        self.register_methods()

    def register_methods(self):
        raise NotImplementedError
