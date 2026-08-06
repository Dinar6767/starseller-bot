import asyncio
import os
from aiogram import Bot, Dispatcher
from app.handlers import router
from app.database.models import async_main

# --- ПРИНУДИТЕЛЬНОЕ СОЗДАНИЕ БАЗЫ ДАННЫХ ПРИ ЗАПУСКЕ ---
print("⏳ Принудительно создаём базу данных перед запуском бота...")
try:
    asyncio.run(async_main())
    print("✅ База данных (таблица orders) успешно создана до старта бота!")
except Exception as e:
    print(f"❌ Ошибка при создании базы: {e}")

# --- ТОКЕНЫ БОТОВ ---
MAIN_BOT_TOKEN = "8897276602:AAEPkqv_eGeY3PSk6uyC0zj5yfz389KFJxs"
ADMIN_BOT_TOKEN = "8849713309:AAFJaikdyfeuggToQ1Yv7fttVn7_WQt0wOI"

# Ваш Telegram ID
ADMIN_ID = 6305430094

# --- ЗАЩИТА БАЗЫ ДАННЫХ (чтобы не терялась на Railway) ---
# Если мы на Railway, создаём папку /app/data для хранения базы
DATA_DIR = "/app/data"
if not os.path.exists(DATA_DIR):
    try:
        os.makedirs(DATA_DIR)
        print(f"✅ Создана папка для данных: {DATA_DIR}")
    except:
        # Если мы не на Railway (например, на компе), просто используем текущую папку
        DATA_DIR = "."

# Указываем путь к файлу базы данных
DB_PATH = os.path.join(DATA_DIR, "db.sqlite3")
os.environ["DB_PATH"] = DB_PATH  # Передаём путь в переменную окружения, чтобы сайт мог её прочитать
print(f"📁 База данных будет сохранена в: {DB_PATH}")

# --- СОЗДАНИЕ БОТОВ ---
bot = Bot(token=MAIN_BOT_TOKEN)
dp = Dispatcher()
dp.include_router(router)

# Второй бот (для уведомлений админу)
admin_bot = Bot(token=ADMIN_BOT_TOKEN)

# --- ФУНКЦИЯ ДЛЯ ОТПРАВКИ УВЕДОМЛЕНИЙ АДМИНУ ---
async def send_admin_notification(text: str, reply_markup=None):
    try:
        await admin_bot.send_message(ADMIN_ID, text, reply_markup=reply_markup)
    except Exception as e:
        print(f"Ошибка уведомления: {e}")

# --- ЗАПУСК БОТА ---
async def main():
    # Строчка await async_main() уже не нужна, база уже создана выше
    await send_admin_notification("✅ Бот StarSeller успешно запущен и готов к работе!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())