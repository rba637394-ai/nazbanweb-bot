from telebot import apihelper
apihelper.API_URL = "https://tapi.bale.ai/bot{0}/{1}"
apihelper.API_FILE_URL = "https://tapi.bale.ai/file/bot{0}/{1}"

import telebot
from telebot import types
import logging
from config import Config
from database import save_user, save_lead, get_all_leads, get_user_count, get_lead_count
from utils import validate_phone, format_lead_message

logger = logging.getLogger(__name__)
bot = telebot.TeleBot(Config.BOT_TOKEN)

user_states = {}

SERVICES = {
    'wordpress': 'طراحی سایت وردپرسی',
    'shop': 'فروشگاه اینترنتی',
    'seo': 'سئو و بهینه سازی',
    'bot': 'ربات بله',
    'landing': 'لندینگ پیج'
}

@bot.message_handler(commands=['start'])
def handle_start(message):
    try:
        save_user(message.from_user.id, message.from_user.username, message.from_user.first_name, message.from_user.last_name)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.add(
            types.KeyboardButton('📋 درخواست مشاوره'),
            types.KeyboardButton('🛠 خدمات ما'),
            types.KeyboardButton('❓ سوالات متداول'),
            types.KeyboardButton('📞 تماس با ما')
        )
        welcome_text = f""" سلام {message.from_user.first_name} عزیز!

به ربات نازبان وب خوش آمدید.

ما خدمات زیر را ارائه می‌دهیم:
• طراحی سایت وردپرسی
• طراحی فروشگاه اینترنتی
• سئو و بهینه سازی
• ساخت ربات اختصاصی بله
• طراحی لندینگ پیج

لطفاً گزینه مورد نظر را انتخاب کنید:"""
        bot.send_message(message.chat.id, welcome_text, reply_markup=markup)
        logger.info(f"✅ کاربر {message.from_user.id} ({message.from_user.first_name}) ربات را استارت کرد")
    except Exception as e:
        logger.error(f"❌ خطا در start: {e}", exc_info=True)

@bot.message_handler(func=lambda m: m.text == '📋 درخواست مشاوره')
def start_consultation(message):
    try:
        user_states[message.from_user.id] = 'waiting_name'
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(types.KeyboardButton(' انصراف'))
        bot.send_message(message.chat.id, "📝 لطفاً نام و نام خانوادگی خود را وارد کنید:", reply_markup=markup)
    except Exception as e:
        logger.error(f"❌ خطا در start_consultation: {e}")

@bot.message_handler(func=lambda m: m.text == '🛠 خدمات ما')
def handle_services(message):
    try:
        services_text = """🛠 *خدمات نازبان وب*

1️⃣ *طراحی سایت وردپرسی*
   • سایت شرکتی و فروشگاهی
   • سریع، امن و واکنش‌گرا
   • آموزش مدیریت سایت

2️ *طراحی فروشگاه اینترنتی*
   • درگاه پرداخت ایرانی
   • بهینه برای موبایل
   • مدیریت آسان محصولات

3️ *سئو و بهینه سازی*
   • سئوی تکنیکال
   • تقویم محتوایی
   • گزارش شفاف ماهانه

4️⃣ *ربات اختصاصی بله*
   • زبان پایتون
   • API رسمی بله
   • اطلاع‌رسانی خودکار

5️⃣ *طراحی لندینگ پیج*
   • طراحی حرفه‌ای
   • بهینه برای تبدیل
   • سرعت بالا

برای مشاوره رایگان، گزینه «درخواست مشاوره» را انتخاب کنید."""
        bot.send_message(message.chat.id, services_text, parse_mode='Markdown')
    except Exception as e:
        logger.error(f"❌ خطا در handle_services: {e}")

@bot.message_handler(func=lambda m: m.text == '❓ سوالات متداول')
def handle_faq(message):
    try:
        faq_text = """❓ *سوالات متداول*

💰 *هزینه طراحی سایت چقدر است؟*
بسته به تعداد صفحات، امکانات و محتوا دارد. بعد از مشاوره رایگان، پیشنهاد دقیق با قیمت شفاف دریافت می‌کنید.

⏱ *ساخت سایت چقدر طول می‌کشه؟*
بسته به محدوده پروژه، معمولاً بین  تا ۶ هفته.

📈 *آیا رتبه گوگل را تضمین می‌کنید؟*
نه؛ هر کس چنین وعده‌ای داد، صادق نیست. ما کار اصولی و گزارش شفاف را تضمین می‌کنیم.

🔧 *بعد از تحویل، سایت را خودم می‌توانم مدیریت کنم؟*
بله؛ جلسه آموزش + مستندات دارید و سایت طوری ساخته می‌شود که به برنامه‌نویس وابسته نباشید.

🛠 *پشتیبانی شامل چه چیزهایی است؟*
یک ماه رفع باگ‌های ناشی از کار ما، رایگان. امکانات جدید با پیش‌فاکتور جدا."""
        bot.send_message(message.chat.id, faq_text, parse_mode='Markdown')
    except Exception as e:
        logger.error(f"❌ خطا در handle_faq: {e}")

@bot.message_handler(func=lambda m: m.text == '📞 تماس با ما')
def handle_contact(message):
    try:
        contact_text = """📞 *راه‌های تماس با نازبان وب*

 *تلفن:* 09102602694

💬 *بله:* @nazbanweb
🔗 کانال: http://ble.ir/nazbanweb

 *تلگرام:* @rba_kh
 کانال: t.me/nazbanweb

📸 *اینستاگرام:* @nazbanweb

🌐 *وب‌سایت:* nazbanweb.ir

برای مشاوره رایگان ۳۰ دقیقه‌ای، گزینه «درخواست مشاوره» را انتخاب کنید."""
        bot.send_message(message.chat.id, contact_text, parse_mode='Markdown')
    except Exception as e:
        logger.error(f"❌ خطا در handle_contact: {e}")

@bot.message_handler(func=lambda m: user_states.get(m.from_user.id) == 'waiting_name')
def get_name(message):
    try:
        if message.text == '❌ انصراف':
            del user_states[message.from_user.id]
            return bot.send_message(message.chat.id, "❌ انصراف ثبت شد.")
        
        if len(message.text.strip()) < 3:
            return bot.send_message(message.chat.id, "⚠️ لطفاً نام کامل خود را وارد کنید (حداقل ۳ حرف).")
        
        user_states[message.from_user.id] = {
            'state': 'waiting_phone',
            'full_name': message.text.strip()
        }
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(types.KeyboardButton('❌ انصراف'))
        bot.send_message(message.chat.id, f"✅ نام ثبت شد: {message.text.strip()}\n\n📱 حالا شماره موبایل خود را وارد کنید (مثال: 09123456789):", reply_markup=markup)
    except Exception as e:
        logger.error(f"❌ خطا در get_name: {e}")

@bot.message_handler(func=lambda m: isinstance(user_states.get(m.from_user.id), dict) and user_states[m.from_user.id].get('state') == 'waiting_phone')
def get_phone(message):
    try:
        if message.text == '❌ انصراف':
            del user_states[message.from_user.id]
            return bot.send_message(message.chat.id, "❌ انصراف ثبت شد.")
        
        phone = validate_phone(message.text)
        if not phone:
            return bot.send_message(message.chat.id, "⚠️ شماره نامعتبر است. لطفاً فرمت صحیح (مثال: 09123456789) را وارد کنید.")
        
        user_states[message.from_user.id]['phone'] = phone
        user_states[message.from_user.id]['state'] = 'waiting_service'
        
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
        for val in SERVICES.values():
            markup.add(types.KeyboardButton(val))
        markup.add(types.KeyboardButton('❌ انصراف'))
        bot.send_message(message.chat.id, "✅ شماره ثبت شد.\n\n🎯 نوع خدمت مورد نظر را انتخاب کنید:", reply_markup=markup)
    except Exception as e:
        logger.error(f"❌ خطا در get_phone: {e}")

@bot.message_handler(func=lambda m: isinstance(user_states.get(m.from_user.id), dict) and user_states[m.from_user.id].get('state') == 'waiting_service')
def get_service(message):
    try:
        if message.text == '❌ انصراف':
            del user_states[message.from_user.id]
            return bot.send_message(message.chat.id, "❌ انصراف ثبت شد.")
        
        if message.text not in SERVICES.values():
            return bot.send_message(message.chat.id, "⚠️ لطفاً فقط یکی از گزینه‌های بالا را انتخاب کنید.")
        
        user_states[message.from_user.id]['service'] = message.text
        user_states[message.from_user.id]['state'] = 'waiting_desc'
        
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(types.KeyboardButton('⏭ بدون توضیحات'), types.KeyboardButton('❌ انصراف'))
        bot.send_message(message.chat.id, f"✅ خدمت انتخاب شد: {message.text}\n\n📝 توضیح کوتاهی درباره پروژه بنویسید (یا 'بدون توضیحات' را بزنید):", reply_markup=markup)
    except Exception as e:
        logger.error(f"❌ خطا در get_service: {e}")

@bot.message_handler(func=lambda m: isinstance(user_states.get(m.from_user.id), dict) and user_states[m.from_user.id].get('state') == 'waiting_desc')
def get_desc(message):
    try:
        if message.text == '❌ انصراف':
            del user_states[message.from_user.id]
            return bot.send_message(message.chat.id, "❌ انصراف ثبت شد.")
        
        data = user_states[message.from_user.id]
        desc = "" if message.text == '⏭ بدون توضیحات' else message.text
        
        lead_id = save_lead(message.from_user.id, data['full_name'], data['phone'], data['service'], desc)
        
        if lead_id:
            confirmation_text = f"""✅ *درخواست شما با موفقیت ثبت شد!*

📋 شناسه درخواست: `{lead_id}`
👤 نام: {data['full_name']}
📱 تلفن: {data['phone']}
🎯 خدمت: {data['service']}

📞 کارشناسان ما در اسرع وقت با شما تماس خواهند گرفت.

ممنون از اعتماد شما به نازبان وب 🙏"""
            bot.send_message(message.chat.id, confirmation_text, parse_mode='Markdown')
            
            try:
                admin_msg = format_lead_message(lead_id, data['full_name'], data['phone'], data['service'], desc, message.from_user.username)
                bot.send_message(Config.ADMIN_ID, admin_msg, parse_mode='Markdown')
                logger.info(f"✅ لید {lead_id} ثبت شد و به ادمین اطلاع داده شد")
            except Exception as e:
                logger.error(f"⚠️ خطا در ارسال نوتیفیکیشن به ادمین: {e}")
        else:
            bot.send_message(message.chat.id, "⚠️ خطایی در ثبت درخواست رخ داد. لطفاً دوباره تلاش کنید.")
        
        del user_states[message.from_user.id]
    except Exception as e:
        logger.error(f"❌ خطا در get_desc: {e}")

@bot.message_handler(commands=['admin'])
def admin_panel(message):
    try:
        if message.from_user.id != Config.ADMIN_ID:
            return bot.send_message(message.chat.id, "⛔ دسترسی غیرمجاز!")
        
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("📊 آمار", callback_data="stats"),
            types.InlineKeyboardButton("📋 لیدها", callback_data="leads")
        )
        bot.send_message(message.chat.id, "🔐 *پنل مدیریت نازبان وب*\n\nگزینه مورد نظر را انتخاب کنید:", reply_markup=markup, parse_mode='Markdown')
    except Exception as e:
        logger.error(f"❌ خطا در admin_panel: {e}")

@bot.callback_query_handler(func=lambda call: call.data in ['stats', 'leads'])
def admin_callbacks(call):
    try:
        if call.from_user.id != Config.ADMIN_ID:
            return bot.answer_callback_query(call.id, "⛔ دسترسی غیرمجاز!")
        
        if call.data == 'stats':
            user_count = get_user_count()
            lead_count = get_lead_count()
            stats_text = f"📊 *آمار ربات*\n\n👥 تعداد کاربران: {user_count}\n📋 تعداد درخواست‌ها: {lead_count}"
            bot.send_message(call.message.chat.id, stats_text, parse_mode='Markdown')
        
        elif call.data == 'leads':
            leads = get_all_leads()
            if not leads:
                return bot.send_message(call.message.chat.id, " هیچ درخواستی ثبت نشده است.")
            
            leads_text = "📋 *آخرین درخواست‌های مشاوره:*\n\n"
            for lead in leads[:10]:
                lead_id, first_name, full_name, phone, service, status, created_at = lead
                leads_text += f" `{lead_id}` | 👤 {full_name} | 📱 `{phone}` | 🎯 {service}\n"
            
            if len(leads) > 10:
                leads_text += f"\n... و {len(leads) - 10} درخواست دیگر"
            
            bot.send_message(call.message.chat.id, leads_text, parse_mode='Markdown')
        
        bot.answer_callback_query(call.id, "✅")
    except Exception as e:
        logger.error(f"❌ خطا در admin_callbacks: {e}")

@bot.message_handler(func=lambda m: True)
def handle_unknown_message(message):
    try:
        if message.from_user.id in user_states:
            return bot.send_message(message.chat.id, "️ لطفاً فقط متن درخواستی را ارسال کنید یا '❌ انصراف' را بزنید.")
        
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.add(
            types.KeyboardButton('📋 درخواست مشاوره'),
            types.KeyboardButton('🛠 خدمات ما'),
            types.KeyboardButton('❓ سوالات متداول'),
            types.KeyboardButton('📞 تماس با ما')
        )
        bot.send_message(message.chat.id, "لطفاً از منوی زیر یکی از گزینه‌ها را انتخاب کنید:", reply_markup=markup)
    except Exception as e:
        logger.error(f"❌ خطا در handle_unknown_message: {e}")