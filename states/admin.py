from telebot.handler_backends import StatesGroup, State


class AdminStates(StatesGroup):
    add_summary_title = State()
    add_summary_content = State()
    add_summary_date = State()

    edit_summary = State()
    edit_summary_title = State()
    edit_summary_content = State()
    edit_summary_date = State()

    approve_delete_summary = State()
    approved_delete_summary = State()
