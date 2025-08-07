from keyboards.inline.view_summary_keyboard import gen_view_summary_keyboard
from keyboards.inline.summaries_list_keyboard import gen_summaries_list_button
from loader import bot
from database.models import db, Notes
from utils import send_note


@bot.callback_query_handler(func=lambda call: call.data == 'list')
def list_summaries(call):
    bot.send_message(call.message.chat.id,
                     'Выбери конспект для просмотра:',
                     reply_markup=gen_summaries_list_button())
    bot.delete_message(call.message.chat.id, call.message.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('summary_'))
def summary_view(call):
    with db.atomic():
        if call.data == 'summary_last':
            note = Notes.select().order_by(Notes.date.desc()).first()
        else:
            note_id = call.data.split('_')[1]
            note = Notes.get_by_id(note_id)

        send_note.send_note(call.message.chat.id, note, gen_view_summary_keyboard(note.id))
        Notes.update(
            views=note.views + 1
        ).where(Notes.id == note.id).execute()
        bot.delete_message(call.message.chat.id, call.message.id)
