from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from database.models import db, Notes
from keyboards.inline.buttons import admin_buttons, users_buttons


def gen_summaries_list_edit_keyboard():
    with db.atomic():
        keyboard = InlineKeyboardMarkup(row_width=1)
        notes = Notes.select().where(Notes.is_deleted == False).order_by(Notes.date.desc())

        for note in notes:
            keyboard.add(InlineKeyboardButton(text=f'📓 {note.title}', callback_data=f'edit_note_{note.id}'))

    keyboard.add(admin_buttons.admin_menu_button)

    return keyboard


def gen_summaries_list_delete_keyboard():
    with db.atomic():
        keyboard = InlineKeyboardMarkup(row_width=1)
        notes = Notes.select().where(Notes.is_deleted == False).order_by(Notes.date.desc())

        for note in notes:
            keyboard.add(InlineKeyboardButton(text=f'🗑 {note.title}', callback_data=f'delete_note_{note.id}'))

    keyboard.add(admin_buttons.admin_menu_button)

    return keyboard


def gen_summaries_list_button():
    with db.atomic():
        keyboard = InlineKeyboardMarkup(row_width=1)
        notes = Notes.select().where(Notes.is_deleted == False).order_by(Notes.date.desc())

        for note in notes:
            keyboard.add(InlineKeyboardButton(text=f'📖 {note.title}', callback_data=f'summary_{note.id}'))

    keyboard.add(users_buttons.menu_button)

    return keyboard