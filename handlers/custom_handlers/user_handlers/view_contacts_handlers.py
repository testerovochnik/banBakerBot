from keyboards.inline.back_main_menu_keyboard import gen_back_main_menu_keyboard
from loader import bot


@bot.callback_query_handler(func=lambda call: call.data == 'contact')
def view_contacts(call):
    bot.send_message(call.message.chat.id,
                     '❤️ @blessedyouthhhh - наш канал\n'
                     '🫡 @germanprts - молодежный пастор\n'
                     '🧑‍💻 @andrewnebolsin - тех.поддержка',
                     reply_markup=gen_back_main_menu_keyboard())
    bot.delete_message(call.message.chat.id, call.message.id)
