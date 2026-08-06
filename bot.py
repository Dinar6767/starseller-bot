import asyncio
from aiogram import Bot, Dispatcher
import os
from app.handlers import router
from app.database.models import async_main

# --- ТОКЕНЫ БОТОВ ---
MAIN_BOT_TOKEN = "8897276602:AAEPkqv_eGeY3PSk6uyC0zj5yfz389KFJxs"
ADMIN_BOT_TOKEN = "8849713309:AAFJaikdyfeuggToQ1Yv7fttVn7_WQt0wOI"

# Ваш Telegram ID
ADMIN_ID = 6305430094

# --- СОЗДАНИЕ БОТОВ ---
bot = Bot(token=MAIN_BOT_TOKEN)
dp = Dispatcher()
dp.include_router(router)

admin_bot = Bot(token=ADMIN_BOT_TOKEN)

# --- ФУНКЦИЯ ДЛЯ ОТПРАВКИ УВЕДОМЛЕНИЙ АДМИНУ ---
async def send_admin_notification(text: str):
    try:
        await admin_bot.send_message(ADMIN_ID, text)
    except Exception as e:
        print(f"Ошибка уведомления: {e}")

# --- ЗАПУСК ---
async def main():
    await async_main()
    await send_admin_notification("✅ Бот StarSeller успешно запущен и готов к работе!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())