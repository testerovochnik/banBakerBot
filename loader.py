from telebot import TeleBot
from telebot.storage import StateMemoryStorage
from config import BOT_TOKEN
from database.models import db, Users, Comments, Notes

state_storage = StateMemoryStorage()

bot = TeleBot(BOT_TOKEN, state_storage=state_storage)

def init_db():
    db.connect()
    db.create_tables([Users, Comments, Notes])
