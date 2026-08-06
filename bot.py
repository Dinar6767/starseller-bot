import asyncio
from aiogram import Bot, Dispatcher
from app.handlers import router
from app.database.models import async_main
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    await async_main()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())