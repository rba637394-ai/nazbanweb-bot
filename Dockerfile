# استفاده از تصویر رسمی پایتون
FROM python:3.11-slim

# تنظیم پوشه کاری
WORKDIR /app

# کپی کردن فایل requirements و نصب کتابخانه‌ها
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# کپی کردن تمام فایل‌های پروژه
COPY . .

# ساخت پوشه برای ذخیره دیتابیس
RUN mkdir -p /app/data

# دستور اجرای ربات
CMD ["python", "main.py"]