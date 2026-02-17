import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.types import Update
import asyncio
import logging

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from app.config import settings
from app.logging_config import setup_logging
from app.handlers.session import router as session_router
from app.handlers.messages import router as messages_router


logger = logging.getLogger(__name__)


async def handle(request: web.Request) -> web.Response:
    try:
        data = await request.json()
    except Exception:
        return web.Response(status=400)
    update = Update(**data)
    dp = request.app['dp']
    await dp.process_update(update)
    return web.Response(text='ok')


async def on_startup(app: web.Application):
    bot = app['bot']
    await bot.set_webhook(settings.WEBHOOK_URL)


async def on_cleanup(app: web.Application):
    bot = app['bot']
    await bot.delete_webhook()


def create_app() -> web.Application:
    setup_logging()
    bot = Bot(settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
    dp = Dispatcher()
    dp.include_router(session_router)
    dp.include_router(messages_router)

    app = web.Application()
    app['bot'] = bot
    app['dp'] = dp
    app.router.add_post(settings.WEBHOOK_PATH, handle)
    app.on_startup.append(on_startup)
    app.on_cleanup.append(on_cleanup)
    return app


async def main():
    setup_logging()
    bot = Bot(settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
    dp = Dispatcher()
    dp.include_router(session_router)
    dp.include_router(messages_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
