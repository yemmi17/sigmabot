from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from app.storage.session_storage import storage

router = Router()


@router.message(Command("session_start"))
async def cmd_start(message: Message):
    chat_id = message.chat.id
    started = storage.start_session(chat_id)
    if started:
        await message.reply("Сессия запущена.")
    else:
        await message.reply(
            "Сессия уже запущена.\nЕсли хотите начать заново, выполните /session_finish"
        )


@router.message(Command("session_finish"))
async def cmd_finish(message: Message):
    chat_id = message.chat.id
    summary = storage.finish_session(chat_id)
    if summary is None:
        await message.reply("Сессия не активна.")
    else:
        text = (
            f"Итоги сессии:\n\nОбщий доход: {summary['total_income']}\n"
            f"Общая комиссия: {summary['total_commission']}\nПрибыль: {summary['profit']}"
        )
        await message.reply(text)
