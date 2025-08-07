from telebot.types import InlineKeyboardMarkup
from keyboards.inline.buttons import users_buttons, admin_buttons
from config import ADMIN_IDS
from database.models import db, Notes


def gen_main_menu_keyboard(user_id):
    keyboard = InlineKeyboardMarkup(row_width=1)
    with db.atomic():
        if Notes.get_or_none():
            keyboard.add(users_buttons.last_summary_button, users_buttons.list_button)

    keyboard.add(users_buttons.contact_button)
    if user_id in ADMIN_IDS:
        keyboard.add(admin_buttons.admin_menu_button)

    return keyboard
