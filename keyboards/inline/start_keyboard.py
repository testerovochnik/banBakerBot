from keyboards.inline.buttons import users_buttons

from telebot.types import InlineKeyboardMarkup


def get_start_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)

    keyboard.add(users_buttons.menu_button)

    return keyboard
