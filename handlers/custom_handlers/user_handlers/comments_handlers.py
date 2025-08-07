from datetime import datetime

from peewee import IntegrityError

from database.models import db, Comments
from keyboards.inline.comments_keyboard import gen_comments_keyboard, gen_add_comment_keyboard
from loader import bot
from states.user import UserState


note_id = 0


@bot.callback_query_handler(func=lambda call: call.data.startswith('comments_'))
def view_comments(call):
    with db.atomic():
        note_id = call.data.split('_')[1]
        comments = Comments.select().where(
                       (Comments.note_id == note_id) &
                       (Comments.is_approved == True)
                   ).order_by(Comments.created_at.desc())
    if comments:
        # Собираем все комментарии в одну строку
        comments_text = "\n\n\n".join(
            f"👤 @{comment.created_by.username}\n"
            f"📅 <i>{comment.created_at.strftime('%d.%m.%Y %H:%M')}</i>\n\n"
            f"💬 {comment.comment}"
            for comment in comments
        )

        # Добавляем заголовок
        message_text = f"📝 Комментарии к конспекту:\n\n{comments_text}"
        bot.send_message(call.message.chat.id,
                         text=message_text,
                         parse_mode='HTML',
                         reply_markup=gen_comments_keyboard(note_id))

    else:
        bot.send_message(call.message.chat.id,
                         '<i>💤 Комментариев пока нет.</i>',
                         parse_mode='HTML',
                         reply_markup=gen_comments_keyboard(note_id))

    bot.delete_message(call.message.chat.id, call.message.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('add_comment_'))
def add_comment(call):
    global note_id
    note_id = call.data.split('_')[2]
    bot.set_state(call.from_user.id, UserState.add_comments)
    bot.send_message(call.message.chat.id,
                     'Отправь комментарий, который хочешь оставить.\n\n'
                     '⚠️ <b>ВНИМАНИЕ!</b> ⚠️ <i>То, что ты отправишь, сразу будет отправлено, как комментарий на модерацию. '
                     'Изменить или удалить комментарий уже будет нельзя.</i>', parse_mode='HTML')
    bot.delete_message(call.message.chat.id, call.message.id)


@bot.message_handler(state=UserState.add_comments)
def save_comments(message):
    global note_id
    try:
        with db.atomic():
            Comments.create(
                note_id=note_id,
                comment=message.text,
                created_at=datetime.now(),
                created_by=message.from_user.id,
            )
        bot.send_message(message.chat.id,
                         '⌛ Комментарий успешно сохранен. '
                         'Он будет отображаться, после обработки модератором.',
                         reply_markup=gen_add_comment_keyboard(note_id))
    except IntegrityError:
        bot.send_message(message.chat.id,
                         '🚫 При сохранении комментария произошла ошибка. Попробуй позже.',
                         reply_markup=gen_add_comment_keyboard(note_id))
    finally:
        bot.delete_message(message.chat.id, message.id)
        bot.delete_message(message.chat.id, message.id - 1)

