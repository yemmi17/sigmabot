import os
import sys
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.config import settings
from app.logging_config import setup_logging
from app.handlers.session import router as session_router
from app.handlers.messages import router as messages_router


logger = logging.getLogger(__name__)


async def main():
    setup_logging()

    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode="HTML"),
    )

    # Удаляем webhook если он вдруг остался
    await bot.delete_webhook(drop_pending_updates=True)

    dp = Dispatcher()

    dp.include_router(session_router)
    dp.include_router(messages_router)

    logger.info("Бот запущен в режиме polling")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
