from datetime import datetime

from peewee import IntegrityError

from keyboards.inline.back_admin_menu_keyboard import gen_back_admin_menu_keyboard
from loader import bot
from keyboards.inline.summaries_list_keyboard import gen_summaries_list_delete_keyboard
from database.models import db, Notes
from states.admin import AdminStates
from utils import send_note

note_id = 0
summary_message = 0


@bot.callback_query_handler(func=lambda call: call.data == 'delete_summary')
def list_for_edit(call):
    bot.send_message(call.message.chat.id,
                     'Выбери конспект, который хочешь изменить:',
                     reply_markup=gen_summaries_list_delete_keyboard())
    bot.delete_message(call.message.chat.id, call.message.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('delete_note_'))
def approve_delete_summary(call):
    global note_id
    note_id = call.data.split('_')[2]
    with db.atomic():
        note = Notes.get_by_id(note_id)
    bot.set_state(call.from_user.id, AdminStates.approve_delete_summary)
    send_note.send_note(call.message.chat.id, note)
    bot.send_message(call.message.chat.id,
                     'Отправь "Удалить", чтобы подтвердить удаление.')
    global summary_message
    summary_message = call.message.id + 1
    bot.delete_message(call.message.chat.id, call.message.id)



@bot.message_handler(state=AdminStates.approve_delete_summary)
def check_approve_delete_summary(message):
    print(message.text.lower())
    if message.text.lower() == 'удалить':
        bot.set_state(message.from_user.id, AdminStates.approved_delete_summary)
        try:
            with db.atomic():
                Notes.update(
                    is_deleted=True,
                    updated_by=message.from_user.id,
                    updated_at=datetime.now()
                ).where(Notes.id == note_id).execute()

            bot.send_message(message.from_user.id,
                             '✅ Конспект успешно удален.',
                             reply_markup=gen_back_admin_menu_keyboard())
            bot.delete_state(message.from_user.id)
            bot.delete_message(message.chat.id, message.id)
            bot.delete_message(message.chat.id, message.id - 1)
            bot.delete_message(message.chat.id, summary_message)

        except IntegrityError:
            bot.send_message(message.from_user.id,
                             f'🚫 При удалении конспекта произошла ошибка. Попробуй позже.',
                             reply_markup=gen_back_admin_menu_keyboard())
            bot.delete_state(message.from_user.id)
            bot.delete_message(message.chat.id, message.id)
            bot.delete_message(message.chat.id, message.id - 1)
            bot.delete_message(message.chat.id, summary_message)
    else:
        bot.send_message(message.from_user.id, 'Отправь "Удалить", чтобы подтвердить удаление.')
        bot.delete_message(message.chat.id, message.id)
        bot.delete_message(message.chat.id, message.id - 1)
        return
