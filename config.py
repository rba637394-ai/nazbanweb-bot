import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    ADMIN_ID = int(os.getenv("ADMIN_ID", 0))
    DB_PATH = os.getenv("DB_PATH", "nazbanweb.db")

    if not BOT_TOKEN:
        raise ValueError("خطای حیاتی: BOT_TOKEN در فایل .env تنظیم نشده است!")
    
    if ADMIN_ID == 0:
        raise ValueError("خطای حیاتی: ADMIN_ID در فایل .env تنظیم نشده است!")