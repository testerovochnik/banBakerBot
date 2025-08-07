from telebot.types import InlineKeyboardButton


admin_menu_button = InlineKeyboardButton(text='💀 Меню админа', callback_data='admin_menu')
add_summary_button = InlineKeyboardButton(text='➕ Добавить конспект', callback_data='add_summary')
edit_summary_button = InlineKeyboardButton(text='✏️ Изменить конспект', callback_data='edit_summary')
delete_summary_button = InlineKeyboardButton(text='🗑 Удалить конспект', callback_data='delete_summary')
moderate_button = InlineKeyboardButton(text='💬 Модерация комментариев', callback_data='moderate')
ban_cancel_button = InlineKeyboardButton(text='🙌 Снять бан с пользователей', callback_data='ban_cancel')
