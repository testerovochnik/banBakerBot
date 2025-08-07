from telebot.types import InlineKeyboardButton


menu_button = InlineKeyboardButton(text='🎯 Главное меню', callback_data='main_menu')
last_summary_button = InlineKeyboardButton(text='📝 Последний конспект', callback_data='summary_last')
list_button = InlineKeyboardButton(text='📚 Список конспектов', callback_data='list')
contact_button = InlineKeyboardButton(text='♥️ Cвязаться с BLESSED', callback_data='contact')
