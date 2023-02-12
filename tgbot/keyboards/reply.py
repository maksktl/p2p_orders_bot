import aiogram.types


class ReplyKeyboard:
    @staticmethod
    def get_keyboard(buttons, resize_keyboard=False, one_time_keyboard=False, selective=False):
        return aiogram.types.ReplyKeyboardMarkup(
            keyboard=[
                [aiogram.types.KeyboardButton(**button) for button in row]
                for row in buttons
            ],
            resize_keyboard=resize_keyboard,
            one_time_keyboard=one_time_keyboard,
            selective=selective
        )

    @staticmethod
    def add_button(keyboard, button_row):
        keyboard.keyboard.append([aiogram.types.KeyboardButton(**button) for button in button_row])
        return keyboard

    @staticmethod
    def remove_row(keyboard, row_index):
        keyboard.keyboard.pop(row_index)
        return keyboard

    @staticmethod
    def remove_button(keyboard, row_index, button_index):
        keyboard.keyboard[row_index].pop(button_index)
        return keyboard

    @staticmethod
    def get_web_app_conf_keyboard(url, config_active=False):
        buttons_row_1 = [{
            'text': '⚙️ Настроить поиск связок',
            'web_app': aiogram.types.WebAppInfo(url=url)
        }]
        if config_active is not None:
            buttons_row_1.append({
                'text': f'{"❌ Отключить" if config_active else "✅ Включить"} поиск связок'
            })
        return ReplyKeyboard.get_keyboard([[*buttons_row_1]], resize_keyboard=True)


"""
>>> keyboard = ReplyKeyboard.get_keyboard([[{"text": "Yes"}, {"text": "No"}], [{"text": "Location", "request_location": True}]])
>>> keyboard = ReplyKeyboard.remove_row(keyboard, 0)
>>> keyboard = ReplyKeyboard.remove_button(keyboard, 0, 0)

"""
