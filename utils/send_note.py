from loader import bot


def send_note(chat_id, note, keyboard=None):
    title = 'Название:'
    summary = 'Конспект:'
    temp_note = (f'_{title}_ *{note.title}*\n'
                             f'_{note.date}_\n\n'
                             f'_{summary}_ {note.content}\n')
    try:
        if note.format_type == 'HTML':
            bot.send_message(chat_id,
                             f'<i>Название:</i> <b>{note.title}</b>\n'
                             f'<i>{note.date}</i>\n\n'
                             f'<i>Конспект:</i> {note.content}\n',
                             parse_mode='HTML', reply_markup=keyboard)
        elif note.format_type == 'Markdown':
            bot.send_message(chat_id, temp_note,
                             parse_mode='MarkdownV2', reply_markup=keyboard)
        else:
            bot.send_message(chat_id, temp_note, reply_markup=keyboard)
    except Exception as e:
        bot.send_message(chat_id, f"⚠️ Ошибка форматирования {e}:\n\n{note.content}", reply_markup=keyboard)
