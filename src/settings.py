import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.environ.get("BOT_TOKEN")
DB_URL = os.environ.get("DB_URL")
SQLITE_DB_NAME = os.environ.get("SQLITE_DB_NAME")
ADMIN_ID = int(os.environ.get("ADMIN_ID"))
