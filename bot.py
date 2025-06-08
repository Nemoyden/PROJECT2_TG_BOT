import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config.settings import BOT_TOKEN
from routers import commands
from routers.handlers import specific_handlers
from middlewares.throttling import ThrottlingMiddleware
from utils.logger import logger

async def main():
  
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    dp.message.middleware(ThrottlingMiddleware())

    dp.include_router(commands.router)
    dp.include_router(specific_handlers.router)

    logger.info("Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
