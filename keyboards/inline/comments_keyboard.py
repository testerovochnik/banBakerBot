from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.buttons import users_buttons


def gen_comments_keyboard(note_id):
    keyboard = InlineKeyboardMarkup(row_width=1)
    add_comment_button = InlineKeyboardButton(text='➕ Добавить комментарий', callback_data=f'add_comment_{note_id}')
    keyboard.add(add_comment_button)
    back_to_summary_button = InlineKeyboardButton(text='⬅️ Назад к конспекту', callback_data=f'summary_{note_id}')
    keyboard.add(back_to_summary_button)
    keyboard.add(users_buttons.menu_button)

    return keyboard


def gen_add_comment_keyboard(note_id):
    keyboard = InlineKeyboardMarkup(row_width=1)
    back_to_summary_button = InlineKeyboardButton(text='⬅️ Назад к конспекту', callback_data=f'summary_{note_id}')
    keyboard.add(back_to_summary_button)
    keyboard.add(users_buttons.menu_button)

    return keyboard
