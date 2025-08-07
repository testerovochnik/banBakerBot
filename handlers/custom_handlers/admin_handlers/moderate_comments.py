from datetime import datetime

from database.models import db, Comments, Users
from keyboards.inline.back_admin_menu_keyboard import gen_back_admin_menu_keyboard
from keyboards.inline.moderate_comments_keyboard import gen_moderate_comments_keyboard, gen_approve_comments_keyboard
from loader import bot


@bot.callback_query_handler(func=lambda call: call.data == 'moderate')
def moderate_comments(call):
    bot.send_message(call.message.chat.id,
                     'Выбери комментарий, который хочешь просмотреть:',
                     reply_markup=gen_moderate_comments_keyboard())

    bot.delete_message(call.message.chat.id, call.message.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('moderate_comments_'))
def approve_comment(call):
    comment_id = call.data.split('_')[-1]
    with db.atomic():
        comment = Comments.select().where(Comments.id == comment_id).get()
        user = Users.select().where(Users.user_id == comment.created_by).get()
    bot.send_message(call.message.chat.id, f'Комментарий для подтверждения:\n\n'
                                           f'@{user.username} - {comment.comment} ({comment.created_at})',
                     reply_markup=gen_approve_comments_keyboard(comment_id))
    bot.delete_message(call.message.chat.id, call.message.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('action_comments_'))
def action_with_comments(call):
    action = call.data.split('_')[-2]
    with db.atomic():
        if action == 'approve':
            Comments.update(
                is_approved=True,
                is_moderated=True,
                moderated_by=call.from_user.id,
                moderated_at=datetime.now()
            ).where(Comments.id == call.data.split('_')[-1]).execute()
            bot.send_message(call.message.chat.id, '✅ Комментарий успешно подтвержден.',
                            reply_markup=gen_back_admin_menu_keyboard())
        elif action == 'delete':
            Comments.update(
                is_moderated=True,
                moderated_by=call.from_user.id,
                moderated_at=datetime.now()
            ).where(Comments.id == call.data.split('_')[-1]).execute()
            bot.send_message(call.message.chat.id, '✅ Комментарий успешно удален.',
                             reply_markup=gen_back_admin_menu_keyboard())
    bot.delete_state(call.from_user.id)
    bot.delete_message(call.message.chat.id, call.message.id)