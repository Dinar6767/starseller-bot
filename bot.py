import asyncio
from aiogram import Bot, Dispatcher
import os
from app.handlers import router
from app.database.models import async_main

# --- ТОКЕНЫ БОТОВ ---
# Токен основного бота (клиентский)
MAIN_BOT_TOKEN = "8897276602:AAEPkqv_eGeY3PSk6uyC0zj5yfz389KFJxs"
# Токен админ-бота (для уведомлений)
ADMIN_BOT_TOKEN = "8849713309:AAFJaikdyfeuggToQ1Yv7fttVn7_WQt0wOI"

# Ваш Telegram ID
ADMIN_ID = 6305430094

# --- СОЗДАНИЕ БОТОВ ---
bot = Bot(token=MAIN_BOT_TOKEN)
dp = Dispatcher()
dp.include_router(router)

# Второй бот (для отправки уведомлений админу)
admin_bot = Bot(token=ADMIN_BOT_TOKEN)

# --- ФУНКЦИЯ ДЛЯ ОТПРАВКИ УВЕДОМЛЕНИЙ АДМИНУ (ТЕПЕРЬ С КНОПКАМИ) ---
async def send_admin_notification(text: str, reply_markup=None):
    """Отправляет сообщение администратору через второго бота"""
    try:
        await admin_bot.send_message(ADMIN_ID, text, reply_markup=reply_markup)
    except Exception as e:
        print(f"Ошибка уведомления: {e}")

# --- ЗАПУСК БОТА ---
async def main():
    await async_main()
    # При запуске отправим тестовое уведомление админу
    await send_admin_notification("✅ Бот StarSeller успешно запущен и готов к работе!")
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())