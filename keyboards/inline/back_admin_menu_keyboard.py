from keyboards.inline.buttons import admin_buttons

from telebot.types import InlineKeyboardMarkup


def gen_back_admin_menu_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(admin_buttons.admin_menu_button)

    return keyboard
