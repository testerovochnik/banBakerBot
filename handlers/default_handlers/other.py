# from telebot.types import Message
#
# from loader import bot
#
#
# @bot.message_handler(func=lambda message: True, priority=100)
# def echo(message: Message):
#     bot.send_message(message.chat.id, 'Я не обрабатываю такие запросы, '
#                                       'но если ты хочешь пообщаться - ты можешь написать нам.\n\n'
#                                       '♥️ /contacts')
#     bot.delete_message(message.chat.id, message.message_id)