from aiogram import Bot

# Токен админ-бота
ADMIN_BOT_TOKEN = "8849713309:AAFJaikdyfeuggToQ1Yv7fttVn7_WQt0wOI"
ADMIN_ID = 6305430094

admin_bot = Bot(token=ADMIN_BOT_TOKEN)

async def send_admin_notification(text: str, reply_markup=None):
    try:
        await admin_bot.send_message(ADMIN_ID, text, reply_markup=reply_markup)
    except Exception as e:
        print(f"Ошибка уведомления: {e}")