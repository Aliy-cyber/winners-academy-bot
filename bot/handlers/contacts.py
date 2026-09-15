from aiogram import Router, F
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.config import (
    PHONE_NUMBER, MANAGER_USERNAME, MANAGER_URL,
    TELEGRAM_CHANNEL, INSTAGRAM, YOUTUBE, WEBSITE,
)
from bot.database import log_action

router = Router(name="contacts")

CONTACT_TEXTS = {
    "📞 Bog'lanish va Tarmoqlar",
    "📞 Bog’lanish va Tarmoqlar",
    "📞 Bog`lanish va Tarmoqlar",
}


@router.message(F.text.in_(CONTACT_TEXTS))
async def show_contacts(message: Message):
    await log_action(message.from_user.id, "📞 Bog'lanish va Tarmoqlar")
    b = InlineKeyboardBuilder()
    b.button(text="📢 Telegram Kanal", url=TELEGRAM_CHANNEL)
    b.button(text="👨‍💼 Menejer", url=MANAGER_URL)
    b.button(text="📸 Instagram", url=INSTAGRAM)
    b.button(text="▶️ YouTube", url=YOUTUBE)
    b.button(text="🌐 Rasmiy Sayt", url=WEBSITE)
    b.adjust(2, 2, 1)

    text = (
        "📞 <b>Bog'lanish va Ijtimoiy Tarmoqlar</b>\n\n"
        "🏆 <b>Winners Academy</b> — Orzularingiz sari birinchi qadam!\n\n"
        f"📞 <b>Telefon:</b> <code>{PHONE_NUMBER}</code>\n"
        f"👨‍💼 <b>Menejer:</b> {MANAGER_USERNAME}\n\n"
        "🌐 <b>Rasmiy sayt:</b> winnersacademy.uz\n"
        "📢 <b>Telegram:</b> @Winners_AcademyUz\n"
        "📸 <b>Instagram:</b> @winners_academyuz\n"
        "▶️ <b>YouTube:</b> @winnersacademyuz\n\n"
        "<i>Quyidagi tugmalar orqali to'g'ridan-to'g'ri o'tishingiz mumkin 👇</i>"
    )
    await message.answer(
        text,
        reply_markup=b.as_markup(),
        disable_web_page_preview=True,
    )

