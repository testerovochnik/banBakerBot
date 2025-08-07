import os

from dotenv import load_dotenv, find_dotenv


if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

load_dotenv()

DB_PATH = "../banBakerBot/data/blessed.db"
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS", "").split(",")))
DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
)

DATE_FORMAT = "%d.%m.%Y"
