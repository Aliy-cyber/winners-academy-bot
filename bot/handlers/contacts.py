from aiogram import Router, F
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.config import (
    PHONE_NUMBER, MANAGER_USERNAME, TELEGRAM_CHANNEL,
    INSTAGRAM, YOUTUBE, WEBSITE,
)
from bot.database import log_action

router = Router(name="contacts")


@router.message(F.text == "\U0001f4de Bog'lanish va Tarmoqlar")
async def show_contacts(message: Message):
    await log_action(message.from_user.id, "\U0001f4de Bog'lanish va Tarmoqlar")
    builder = InlineKeyboardBuilder()
    builder.button(text="\U0001f4e2 Telegram Kanal", url=TELEGRAM_CHANNEL)
    builder.button(text="\U0001f4f8 Instagram", url=INSTAGRAM)
    builder.button(text="\u25b6\ufe0f YouTube", url=YOUTUBE)
    builder.button(text="\U0001f310 Rasmiy Sayt", url=WEBSITE)
    builder.button(text="\u2b50\ufe0f O'quvchilar Natijalari", url=TELEGRAM_CHANNEL)
    builder.adjust(2, 2, 1)
    text = (
        "\U0001f4de <b>Bog'lanish va Ijtimoiy Tarmoqlar</b>\n\n"
        f"\U0001f4de <b>Telefon:</b> {PHONE_NUMBER}\n"
        f"\U0001f468\u200d\U0001f4bc <b>Menejer:</b> {MANAGER_USERNAME}\n\n"
        "\U0001f517 <b>Ijtimoiy tarmoqlarimiz:</b>"
    )
    await message.answer(text, reply_markup=builder.as_markup(), disable_web_page_preview=True)
