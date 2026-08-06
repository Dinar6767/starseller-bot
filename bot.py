import asyncio
import os
from aiogram import Bot, Dispatcher
from app.handlers import router
from app.database.models import async_main

# --- ТОКЕНЫ БОТОВ ---
MAIN_BOT_TOKEN = "8897276602:AAEPkqv_eGeY3PSk6uyC0zj5yfz389KFJxs"
ADMIN_BOT_TOKEN = "8849713309:AAFJaikdyfeuggToQ1Yv7fttVn7_WQt0wOI"

# Ваш Telegram ID
ADMIN_ID = 6305430094

# --- ЗАЩИТА БАЗЫ ДАННЫХ (чтобы не терялась на Railway) ---
DATA_DIR = "/app/data"
if not os.path.exists(DATA_DIR):
    try:
        os.makedirs(DATA_DIR)
        print(f"✅ Создана папка для данных: {DATA_DIR}")
    except:
        DATA_DIR = "."

DB_PATH = os.path.join(DATA_DIR, "db.sqlite3")
os.environ["DB_PATH"] = DB_PATH
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

# === НОВАЯ ФУНКЦИЯ ДЛЯ ОТПРАВКИ ЗАКАЗА АДМИНУ С КНОПКАМИ ===
async def send_order_notification(amount: int, username: str, order_id: int):
    """
    Эта функция отправляет уведомление админу с кнопками.
    Вызывается и из бота, и с сайта.
    """
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

    text = (
        f"🛒 **НОВЫЙ ЗАКАЗ!**\n"
        f"⭐ Количество: {amount}\n"
        f"👤 Получатель: @{username}\n"
        f"🆔 Заказ: {order_id}"
    )
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Подтвердить оплату", callback_data=f"adm_conf:{order_id}"),
            InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")
        ]
    ])
    
    await send_admin_notification(text, reply_markup=keyboard)

# --- ЗАПУСК БОТА ---
async def main():
    await async_main()
    await send_admin_notification("✅ Бот StarSeller успешно запущен и готов к работе!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())