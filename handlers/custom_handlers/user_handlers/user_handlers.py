from loader import bot
from database.models import db, Notes
from keyboards.inline.main_menu_keyboard import gen_main_menu_keyboard


@bot.callback_query_handler(func=lambda callback_query: callback_query.data == 'main_menu')
def main_menu(callback_query):

    with db.atomic():
        if Notes.get_or_none():
            bot.send_message(callback_query.message.chat.id,
                             'Главное меню ⬇️',
                             reply_markup=gen_main_menu_keyboard(callback_query.from_user.id))
        else:
            bot.send_message(callback_query.message.chat.id,
                             'В данный момент, конспекты еще не добавлены... Но скоро они будут.'
                                                   '\nПока можешь связаться с нами и подписаться на наш канал ⬇️',
                             reply_markup=gen_main_menu_keyboard(callback_query.from_user.id))

        bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
