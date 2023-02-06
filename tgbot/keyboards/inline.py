import aiogram.types


class InlineKeyboard:
    @staticmethod
    def get_keyboard(buttons):
        return aiogram.types.InlineKeyboardMarkup(
            inline_keyboard=[
                [aiogram.types.InlineKeyboardButton(**button) for button in row]
                for row in buttons
            ]
        )

    @staticmethod
    def add_button(keyboard, button_row):
        keyboard.inline_keyboard.append([aiogram.types.InlineKeyboardButton(**button) for button in button_row])
        return keyboard

    @staticmethod
    def remove_row(keyboard, row_index):
        keyboard.inline_keyboard.pop(row_index)
        return keyboard

    @staticmethod
    def remove_button(keyboard, row_index, button_index):
        keyboard.inline_keyboard[row_index].pop(button_index)
        return keyboard


"""
>>> keyboard = InlineKeyboard.get_keyboard([[{"text": "Google", "url": "https://www.google.com/"}], [{"text": "Yandex", "url": "https://www.yandex.ru/"}]])
>>> keyboard = InlineKeyboard.remove_row(keyboard, 0)
>>> keyboard = InlineKeyboard.remove_button(keyboard, 0, 0)
"""
