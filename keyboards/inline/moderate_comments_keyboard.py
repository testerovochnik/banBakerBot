from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from database.models import Comments, db
from keyboards.inline.buttons import admin_buttons


def gen_moderate_comments_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    with db.atomic():
        comments = Comments.select().where(Comments.is_moderated == False).order_by(Comments.created_at.asc())
        for comment in comments:
            comment_button = InlineKeyboardButton(text=f'{comment.comment}', callback_data=f'moderate_comments_{comment.id}')
            keyboard.add(comment_button)
    keyboard.add(admin_buttons.admin_menu_button)
    return keyboard


def gen_approve_comments_keyboard(comment_id):
    keyboard = InlineKeyboardMarkup(row_width=1)
    approve_button = InlineKeyboardButton(text='✅ Подтвердить', callback_data=f'action_comments_approve_{comment_id}')
    delete_button = InlineKeyboardButton(text='❌ Удалить', callback_data=f'action_comments_delete_{comment_id}')
    keyboard.add(approve_button)
    keyboard.add(delete_button)
    keyboard.add(admin_buttons.admin_menu_button)

    return keyboard