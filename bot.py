import asyncio
import os
from aiogram import Bot, Dispatcher
from app.handlers import router
from app.database.models import async_main
from notify import send_admin_notification

# ТОКЕНЫ
MAIN_BOT_TOKEN = "8897276602:AAEPkqv_eGeY3PSk6uyC0zj5yfz389KFJxs"
ADMIN_BOT_TOKEN = "8849713309:AAFJaikdyfeuggToQ1Yv7fttVn7_WQt0wOI"

# ВАШ ID
ADMIN_ID = 6305430094

# БАЗА ДАННЫХ
DATA_DIR = "/app/data"
if not os.path.exists(DATA_DIR):
    try:
        os.makedirs(DATA_DIR)
    except:
        DATA_DIR = "."

DB_PATH = os.path.join(DATA_DIR, "db.sqlite3")
os.environ["DB_PATH"] = DB_PATH

bot = Bot(token=MAIN_BOT_TOKEN)
dp = Dispatcher()
dp.include_router(router)

async def main():
    await async_main()
    await send_admin_notification("✅ Бот StarSeller запущен и готов!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())