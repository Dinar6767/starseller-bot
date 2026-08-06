from aiogram import Bot

# Токен вашего админ-бота (уведомителя)
ADMIN_BOT_TOKEN = "8849713309:AAFJaikdyfeuggToQ1Yv7fttVn7_WQt0wOI"
ADMIN_ID = 6305430094

# Создаем отдельного бота для отправки уведомлений
admin_bot = Bot(token=ADMIN_BOT_TOKEN)

# Функция уведомлений (она теперь живет в этом отдельном файле)
async def send_admin_notification(text: str, reply_markup=None):
    try:
        await admin_bot.send_message(ADMIN_ID, text, reply_markup=reply_markup)
    except Exception as e:
        print(f"Ошибка уведомления: {e}")