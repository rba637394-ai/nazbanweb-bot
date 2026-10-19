import logging
import os
from config import Config
from database import init_db
from handlers import bot

# تنظیمات لاگینگ برای نمایش پیام‌ها در ترمینال و ذخیره در فایل
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("bot.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("NazbanWebBot")

def main():
    logger.info("🚀 ربات نازبان وب در حال راه‌اندازی است...")
    try:
        # ساخت دیتابیس اگر وجود نداشته باشد
        init_db()
        
        logger.info("✅ دیتابیس آماده شد. ربات در حال گوش دادن به پیام‌ها است...")
        
        # شروع ربات (این خط باعث می‌شود ربات همیشه روشن بماند)
        bot.infinity_polling(timeout=60, long_polling_timeout=60)
        
    except Exception as e:
        logger.error(f"❌ خطای حیاتی در راه‌اندازی ربات: {e}", exc_info=True)

if __name__ == "__main__":
    main()