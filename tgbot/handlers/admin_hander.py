from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.handlers.base import BaseHandler
from tgbot.keyboards.reply import ReplyKeyboard
from tgbot.services.user_service import UserService


class AdminHandler(BaseHandler):
    def __init__(self, dp: Dispatcher):
        self._general_filters = {"bot_access": True, 'is_admin': True}
        super().__init__(dp)

    @staticmethod
    async def admin_start(message: Message, config, config_active):
        await message.reply("Здравствуйте, уважаемый администратор.\n"
                            "Чтобы посмотреть список команд, отправьте боту /help",
                            reply_markup=ReplyKeyboard.get_web_app_conf_keyboard(config.tg_bot.webapp_url,
                                                                                 config_active)
                            )

    @staticmethod
    async def help(message: Message):
        await message.answer("Помощь:\n\n"
                             "/grant_access user_id - Дать пользователю права на доступ к боту\n"
                             "/revoke_access user_id - Отобрать у пользователя права на доступ к боту\n\n"
                             "/promote user_id - Выдать пользовтелю права администратора\n"
                             "/revoke_promote user_id - Отобрать у пользователя права администратора")

    @staticmethod
    async def grant_access(message: Message):
        command, user_tg_id = message.text.split()
        user_tg_id = int(user_tg_id)
        bot_access = '/grant_access' == command
        await UserService.get_instance().set_user_settings(user_tg_id, bot_access=bot_access)
        await message.answer(
            f'<a href="tg://user?id={user_tg_id}">Пользователь</a> {"получил" if bot_access else "потерял"} доступ к боту')

    @staticmethod
    async def promote_user(message: Message):
        command, user_tg_id = message.text.split()
        user_tg_id = int(user_tg_id)
        admin = '/promote' == command
        await UserService.get_instance().set_user_settings(user_tg_id, admin=admin)
        await message.answer(
            f'<a href="tg://user?id={user_tg_id}">Пользователь</a> {"получил" if admin else "потерял"} права администратора')

    def register_methods(self):
        self.dp.register_message_handler(AdminHandler.admin_start, commands=['start'], state='*',
                                         **self._general_filters)
        self.dp.register_message_handler(AdminHandler.help, commands=['help'], state='*',
                                         **self._general_filters)
        self.dp.register_message_handler(AdminHandler.grant_access, commands=['grant_access'], state='*',
                                         **self._general_filters)
        self.dp.register_message_handler(AdminHandler.promote_user, commands=['promote'], state='*',
                                         **self._general_filters)
        self.dp.register_message_handler(AdminHandler.grant_access, commands=['revoke_access'], state='*',
                                         **self._general_filters)
        self.dp.register_message_handler(AdminHandler.promote_user, commands=['revoke_promote'], state='*',
                                         **self._general_filters)
