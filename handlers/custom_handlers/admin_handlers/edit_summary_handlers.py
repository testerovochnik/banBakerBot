from datetime import datetime

from peewee import IntegrityError

from config import DATE_FORMAT
from database.models import db, Notes
from keyboards.inline.back_admin_menu_keyboard import gen_back_admin_menu_keyboard
from loader import bot
from keyboards.inline.summaries_list_keyboard import gen_summaries_list_edit_keyboard
from states.admin import AdminStates
from utils import send_note


summary_message = 0
note_id = 0


@bot.callback_query_handler(func=lambda call: call.data == 'edit_summary')
def list_for_edit(call):
    bot.send_message(call.message.chat.id,
                     'Выбери конспект, который хочешь изменить:',
                     reply_markup=gen_summaries_list_edit_keyboard())
    bot.delete_message(call.message.chat.id, call.message.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('edit_note_'))
def edit_summary(call):
    global note_id
    note_id = call.data.split('_')[2]
    with db.atomic():
        note = Notes.get_by_id(note_id)
    bot.set_state(call.from_user.id, AdminStates.edit_summary_title)
    send_note.send_note(call.message.chat.id, note)
    bot.send_message(call.message.chat.id,
                     'Введи новое название конспекта в формате:\n'
                     'Название проповеди - Проповедник.')
    bot.delete_message(call.message.chat.id, call.message.id)


@bot.message_handler(state=AdminStates.edit_summary_title)
def edit_summary_title(message):
    title = message.text
    if len(title.split(' - ')) == 2:
        bot.set_state(message.from_user.id, AdminStates.edit_summary_content)
        bot.send_message(message.chat.id,
                         'Отправь конспект с форматированием')
        bot.delete_message(message.chat.id, message.id)
        bot.delete_message(message.chat.id, message.id - 1)
        global summary_message
        summary_message = message.id - 2

    else:
        bot.send_message(message.chat.id,
                         'Отправь название конспекта в формате:'
                         '\nНазвание проповеди - Проповедник')
        bot.delete_message(message.chat.id, message.id)
        bot.delete_message(message.chat.id, message.id - 1)
        return

    with bot.retrieve_data(message.from_user.id) as data:
        data['new_summary'] = {'title': title}


@bot.message_handler(state=AdminStates.edit_summary_content)
def edit_summary_content(message):
    content = message.text
    bot.set_state(message.from_user.id, AdminStates.edit_summary_date)
    bot.send_message(message.chat.id,
                     'Отправь дату проповеди в формате: ДД.ММ.ГГГГ')
    bot.delete_message(message.chat.id, message.id)
    bot.delete_message(message.chat.id, message.id - 1)

    with bot.retrieve_data(message.from_user.id) as data:
        data['new_summary']['content'] = content


@bot.message_handler(state=AdminStates.edit_summary_date)
def edit_summary_date(message):
    due_date_string = message.text
    try:
        date = datetime.strptime(due_date_string, DATE_FORMAT)
    except ValueError:
        bot.send_message(message.from_user.id, "Введите дату (ДД.ММ.ГГГГ):")
        bot.delete_message(message.chat.id, message.id)
        bot.delete_message(message.chat.id, message.id - 1)
        return

    with bot.retrieve_data(message.from_user.id) as data:
        data['new_summary']['date'] = date

    try:
        with db.atomic():
            Notes.update(
                title=data['new_summary']['title'],
                content=data['new_summary']['content'],
                date=data['new_summary']['date'],
                updated_by=message.from_user.id,
                updated_at=datetime.now()
            ).where(Notes.id == note_id).execute()

        bot.send_message(message.from_user.id,
                         '✅ Конспект успешно отредактирован.',
                         reply_markup=gen_back_admin_menu_keyboard())
        bot.delete_state(message.from_user.id)
        bot.delete_message(message.chat.id, message.id)
        bot.delete_message(message.chat.id, message.id - 1)
        bot.delete_message(message.chat.id, summary_message)

    except IntegrityError:
        bot.send_message(message.from_user.id,
                         f'🚫 При редактировании конспекта произошла ошибка. Попробуй позже.',
                         reply_markup=gen_back_admin_menu_keyboard())
        bot.delete_state(message.from_user.id)
        bot.delete_message(message.chat.id, message.id)
        bot.delete_message(message.chat.id, message.id - 1)
        bot.delete_message(message.chat.id, summary_message)
