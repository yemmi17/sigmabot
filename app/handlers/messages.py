from aiogram import Router
from aiogram.types import Message
from app.services.parser import parse_caption
from app.storage.session_storage import storage

router = Router()


@router.message()
async def photo_handler(message: Message):
    if not message.photo:
        return

    chat_id = message.chat.id
    thread_id = message.message_thread_id

    if not storage.is_active(chat_id, thread_id):
        return

    caption = message.caption
    if not caption:
        await message.reply("Данные не учтены: отсутствует подпись.")
        return

    try:
        income, commission = parse_caption(caption)
    except ValueError as e:
        code = str(e)
        if code == "format":
            await message.reply("Неверный формат.\nИспользуйте: доход / комиссия")
        elif code == "commission_gt_income":
            await message.reply(
                "Комиссия больше дохода.\nПроверьте порядок чисел.\nФормат: доход / комиссия"
            )
        elif code == "income_positive":
            await message.reply("Неверный формат.\nДоход должен быть больше 0.")
        elif code == "commission_nonnegative":
            await message.reply("Неверный формат.\nКомиссия должна быть >= 0.")
        else:
            await message.reply("Неверный формат.\nИспользуйте: доход / комиссия")
        return

    storage.add_entry(chat_id, thread_id, income, commission)

    await message.reply("Данные учтены.")
