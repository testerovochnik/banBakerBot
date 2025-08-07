from keyboards.inline.buttons import admin_buttons, users_buttons
from database.models import db, Comments, Users

from telebot.types import InlineKeyboardMarkup


def gen_admin_menu_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(admin_buttons.add_summary_button, admin_buttons.edit_summary_button,
                 admin_buttons.delete_summary_button)

    with db.atomic():
        if Comments.get_or_none(Comments.is_moderated == False):
            keyboard.add(admin_buttons.moderate_button)
        if Users.get_or_none(Users.is_banned == True):
            keyboard.add(admin_buttons.ban_cancel_button)

    keyboard.add(users_buttons.menu_button)
    return keyboard
