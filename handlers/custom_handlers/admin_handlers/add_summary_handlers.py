from datetime import datetime

from peewee import IntegrityError

import html
from config import DATE_FORMAT
from database.models import db, Notes
from keyboards.inline.back_admin_menu_keyboard import gen_back_admin_menu_keyboard

from loader import bot
from states.admin import AdminStates


def convert_to_html(text, entities):
    result = []
    last_pos = 0

    for entity in entities:
        # Текст до форматирования
        result.append(html.escape(text[last_pos:entity.offset]))

        # Форматированный фрагмент
        fragment = text[entity.offset:entity.offset + entity.length]

        if entity.type == 'bold':
            result.append(f'<b>{html.escape(fragment)}</b>')
        elif entity.type == 'italic':
            result.append(f'<i>{html.escape(fragment)}</i>')
        elif entity.type == 'underline':
            result.append(f'<u>{html.escape(fragment)}</u>')
        elif entity.type == 'strikethrough':
            result.append(f'<s>{html.escape(fragment)}</s>')
        elif entity.type == 'code':
            result.append(f'<code>{html.escape(fragment)}</code>')
        else:
            result.append(html.escape(fragment))

        last_pos = entity.offset + entity.length

    # Остаток текста
    result.append(html.escape(text[last_pos:]))

    return ''.join(result)


@bot.callback_query_handler(func=lambda call: call.data == 'add_summary')
def add_summary(call):
    bot.set_state(call.from_user.id, AdminStates.add_summary_title)
    bot.send_message(call.message.chat.id,
                     'Отправь название конспекта в формате:'
                     '\nНазвание проповеди - Проповедник')
    bot.delete_message(call.message.chat.id, call.message.id)


@bot.message_handler(state=AdminStates.add_summary_title)
def add_summary_title(message):

    title = message.text
    if len(title.split(' - ')) == 2:
        bot.set_state(message.from_user.id, AdminStates.add_summary_content)
        bot.send_message(message.chat.id,
                         'Отправь конспект с форматированием')
        bot.delete_message(message.chat.id, message.id)
        bot.delete_message(message.chat.id, message.id - 1)

    else:
        bot.send_message(message.chat.id,
                         'Отправь название конспекта в формате:'
                         '\nНазвание проповеди - Проповедник')
        bot.delete_message(message.chat.id, message.id)
        bot.delete_message(message.chat.id, message.id - 1)
        return

    with bot.retrieve_data(message.from_user.id) as data:
        data['new_summary'] = {'title': title}


@bot.message_handler(state=AdminStates.add_summary_content)
def add_summary_content(message):
    bot.set_state(message.from_user.id, AdminStates.add_summary_date)
    bot.send_message(message.chat.id,
                     'Отправь дату проповеди в формате: ДД.ММ.ГГГГ')
    bot.delete_message(message.chat.id, message.id)
    bot.delete_message(message.chat.id, message.id - 1)

    if message.entities or message.caption_entities:
        parse_mode = 'HTML'
        formatted_text = convert_to_html(message.text, message.entities)
    else:
        parse_mode = None
        formatted_text = message.text

    with bot.retrieve_data(message.from_user.id) as data:
        data['new_summary']['content'] = formatted_text
        data['new_summary']['format_type'] = parse_mode or 'plain'


@bot.message_handler(state=AdminStates.add_summary_date)
def add_summary_date(message):
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
            Notes.create(
                title=data['new_summary']['title'],
                content=data['new_summary']['content'],
                date=data['new_summary']['date'],
                format_type=data['new_summary']['format_type'],
                created_by=message.from_user.id,
                created_at=datetime.now()
            )

        bot.send_message(message.from_user.id,
                         '✅ Конспект успешно добавлен.',
                         reply_markup=gen_back_admin_menu_keyboard())
        bot.delete_state(message.from_user.id)
        bot.delete_message(message.chat.id, message.id)
        bot.delete_message(message.chat.id, message.id - 1)
    except IntegrityError:
        bot.send_message(message.from_user.id,
                         f'🚫 При добавлении конспекта произошла ошибка. Попробуй позже.',
                         reply_markup=gen_back_admin_menu_keyboard())
        bot.delete_state(message.from_user.id)
        bot.delete_message(message.chat.id, message.id)
        bot.delete_message(message.chat.id, message.id - 1)
