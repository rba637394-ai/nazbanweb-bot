import re

def validate_phone(phone):
    phone = re.sub(r'\D', '', str(phone))
    if phone.startswith('0'):
        phone = phone[1:]
    if re.match(r'^9\d{9}$', phone):
        return '0' + phone
    return None

def format_lead_message(lead_id, full_name, phone, service_type, description, username=None):
    msg = f"🔔 *درخواست مشاوره جدید*\n\n شناسه: `{lead_id}`\n نام: {full_name}\n📱 تلفن: `{phone}`\n🎯 خدمت: {service_type}\n"
    if username:
        msg += f"👤 یوزرنیم: @{username}\n"
    if description:
        msg += f"\n📝 توضیحات:\n{description}\n"
    return msg + "\n✅ برای پیگیری با مشتری تماس بگیرید."