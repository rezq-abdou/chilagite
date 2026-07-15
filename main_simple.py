import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from handlers import router

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN", "8845307308:AAE70czwCM4-T_Xo8AWV5-FkOXYv08aO2Lk")

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="Markdown"))
dp = Dispatcher()

async def main():
    dp.include_router(router)
    try:
        await bot.delete_webhook(drop_pending_updates=True)
    except Exception:
        pass
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped")
    except Exception as e:
        logging.error(f"Error: {e}")
