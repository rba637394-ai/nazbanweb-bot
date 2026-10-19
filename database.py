import sqlite3
import logging
from config import Config

logger = logging.getLogger(__name__)

def init_db():
    try:
        conn = sqlite3.connect(Config.DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            full_name TEXT,
            phone TEXT,
            service_type TEXT,
            description TEXT,
            status TEXT DEFAULT 'جدید',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id))''')
        conn.commit()
        conn.close()
        logger.info("✅ دیتابیس با موفقیت آماده شد")
    except Exception as e:
        logger.error(f"❌ خطا در دیتابیس: {e}", exc_info=True)

def save_user(user_id, username, first_name, last_name):
    try:
        conn = sqlite3.connect(Config.DB_PATH)
        cursor = conn.cursor()
        cursor.execute('INSERT OR REPLACE INTO users (user_id, username, first_name, last_name) VALUES (?, ?, ?, ?)',
                       (user_id, username, first_name, last_name))
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(f"❌ خطا در ذخیره کاربر: {e}")

def save_lead(user_id, full_name, phone, service_type, description):
    try:
        conn = sqlite3.connect(Config.DB_PATH)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO leads (user_id, full_name, phone, service_type, description) VALUES (?, ?, ?, ?, ?)',
                       (user_id, full_name, phone, service_type, description))
        lead_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return lead_id
    except Exception as e:
        logger.error(f"❌ خطا در ذخیره لید: {e}")
        return None

def get_all_leads():
    try:
        conn = sqlite3.connect(Config.DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT l.id, u.first_name, l.full_name, l.phone, l.service_type, l.status, l.created_at FROM leads l JOIN users u ON l.user_id = u.user_id ORDER BY l.created_at DESC')
        leads = cursor.fetchall()
        conn.close()
        return leads
    except Exception as e:
        logger.error(f" خطا در دریافت لیدها: {e}")
        return []

def get_user_count():
    try:
        conn = sqlite3.connect(Config.DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM users')
        count = cursor.fetchone()[0]
        conn.close()
        return count
    except:
        return 0

def get_lead_count():
    try:
        conn = sqlite3.connect(Config.DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM leads')
        count = cursor.fetchone()[0]
        conn.close()
        return count
    except:
        return 0