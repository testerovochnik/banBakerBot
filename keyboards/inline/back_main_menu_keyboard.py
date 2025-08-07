from keyboards.inline.buttons import users_buttons

from telebot.types import InlineKeyboardMarkup


def gen_back_main_menu_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(users_buttons.menu_button)

    return keyboard