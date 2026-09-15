from aiogram import Router, F
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.config import (
    PHONE_NUMBER, MANAGER_USERNAME,
    TELEGRAM_CHANNEL, INSTAGRAM, YOUTUBE, WEBSITE,
)
from bot.database import log_action

router = Router(name="contacts")

CONTACT_TEXTS = {
    "\U0001f4de Bog'lanish va Tarmoqlar",
    "\U0001f4de Bog\u2019lanish va Tarmoqlar",
}


@router.message(F.text.in_(CONTACT_TEXTS))
async def show_contacts(message: Message):
    await log_action(message.from_user.id, "\U0001f4de Bog'lanish va Tarmoqlar")
    b = InlineKeyboardBuilder()
    b.button(text="\U0001f4e2 Telegram Kanal",        url=TELEGRAM_CHANNEL)
    b.button(text="\U0001f4f8 Instagram",              url=INSTAGRAM)
    b.button(text="\u25b6\ufe0f YouTube",             url=YOUTUBE)
    b.button(text="\U0001f310 Rasmiy Sayt",            url=WEBSITE)
    b.button(text="\U0001f4de Qo'ng'iroq qilish",      url=f"tel:{PHONE_NUMBER}")
    b.adjust(2, 2, 1)
    await message.answer(
        "\U0001f4de <b>Bog'lanish va Ijtimoiy Tarmoqlar</b>\n\n"
        f"\U0001f4de <b>Telefon:</b> {PHONE_NUMBER}\n"
        f"\U0001f468\u200d\U0001f4bc <b>Menejer:</b> {MANAGER_USERNAME}\n\n"
        "\U0001f517 <b>Ijtimoiy tarmoqlar:</b>",
        reply_markup=b.as_markup(),
        disable_web_page_preview=True,
    )
