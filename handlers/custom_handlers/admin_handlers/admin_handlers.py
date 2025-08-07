from loader import bot
from keyboards.inline.admin_menu_keyboard import gen_admin_menu_keyboard


@bot.callback_query_handler(func=lambda call: call.data == 'admin_menu')
def admin_menu(call):
    bot.delete_state(call.message.from_user.id)
    bot.send_message(call.message.chat.id,
                     'Добро пожаловать в режим администратора! \n'
                     'Помни, что с большей силой приходит, большая ответственность!\n'
                     'Постарайся быть аккуратнее!',
                     reply_markup=gen_admin_menu_keyboard()
                     )
    bot.delete_message(call.message.chat.id, call.message.id)
