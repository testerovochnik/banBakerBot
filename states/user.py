from telebot.handler_backends import StatesGroup, State


class UserState(StatesGroup):
    view_last_summary = State()
    view_list_summaries = State()
    view_selected_summary = State()
    view_comments = State()
    add_comments = State()
    delete_comments = State()
