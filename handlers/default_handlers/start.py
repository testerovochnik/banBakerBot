from loader import bot
from database.models import db, Users
from keyboards.inline.start_keyboard import get_start_keyboard

from telebot.types import Message


@bot.message_handler(commands=['start'])
def start(message: Message) -> None:
    try:
        with db.atomic():
            if not Users.get_or_none(Users.user_id == message.from_user.id):
                Users.create(
                    user_id=message.from_user.id,
                    username=message.from_user.username,
                )
            elif not Users.get_or_none((Users.user_id == message.from_user.id) &
                                       (Users.username == message.from_user.username)):
                Users.update(
                    username=message.from_user.username
                ).where(
                    Users.user_id == message.from_user.id
                ).execute()
                
    finally:
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}.\n'
                                          f'Я Бэн Пекарь - хранитель историй. '
                                          f'Здесь ты сможешь почитать все конспекты с молодежек.\n\n'
                                          f'Переходи в меню ⬇️', reply_markup=get_start_keyboard())
        bot.delete_message(message.chat.id, message.message_id)
