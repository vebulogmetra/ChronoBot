from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.environ.get("BOT_TOKEN")
DB_URL = os.environ.get("DB_URL")
SQLITE_DB_NAME = os.environ.get("SQLITE_DB_NAME")
ADMIN_ID = os.environ.get("ADMIN_ID")
