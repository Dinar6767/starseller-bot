import asyncio
from aiogram import Bot, Dispatcher
from app.handlers import router
from app.database.models import async_main

# === ПРОКСИ ДЛЯ ОБХОДА БЛОКИРОВОК (ПРАВИЛЬНЫЙ СПОСОБ ДЛЯ AIOGRAM 3) ===
PROXY_URL = "http://188.213.168.127:8080"

# Твой токен
TOKEN = "8897276602:AAEPkqv_eGeY3PSk6uyC0zj5yfz389KFJxs"

async def main():
    # Передаем прокси напрямую в Bot, без создания session
    bot = Bot(token=TOKEN, proxy=PROXY_URL)
    dp = Dispatcher()
    dp.include_router(router)

    await async_main()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())