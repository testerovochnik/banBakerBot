from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.buttons import users_buttons


def gen_view_summary_keyboard(note_id):
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton(text=f'💬 Комментарии', callback_data=f'comments_{note_id}'))
    keyboard.add(users_buttons.menu_button)

    return keyboard
