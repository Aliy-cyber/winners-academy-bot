from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.config import WEBAPP_URL
from bot.keyboards.reply import main_menu_keyboard
from bot.keyboards.inline import cta_register_keyboard
from bot.database import save_user, log_action

router = Router(name="start")

START_TEXT = (
    "\U0001f44b Assalomu alaykum, <b>{name}</b>!\n\n"
    "\U0001f3c6 <b>Winners Academy</b> rasmiy botiga xush kelibsiz!\n\n"
    "Biz Surxondaryoda <b>9 yillik tajriba</b> va <b>7 ta filial</b>ga ega, "
    "minglab o'quvchilarni IELTS va xalqaro marralarga olib chiqqan yetakchi akademiya.\n\n"
    "\U0001f4ca <b>Natijalarimiz:</b>\n"
    "\u2022 3000+ muvaffaqiyatli o'quvchi\n"
    "\u2022 IELTS 8.5 \u2014 eng yuqori ball\n"
    "\u2022 50% Grant eng yaxshi o'quvchilarga\n"
    "\u2022 2+1 ta o'qituvchi nazoratida\n\n"
    "\U0001f447 <b>Quyidagi menyudan tanlang:</b>"
)

REGISTER_PROMPT = (
    "\U0001f680 <b>Sinov darsiga yozilish</b>\n\n"
    "Birinchi dars <b>BEPUL!</b>\n"
    "Quyidagi tugmani bosing va ro'yxatdan o'ting \U0001f447"
)


@router.message(CommandStart())
async def cmd_start(message: Message):
    user = message.from_user
    await save_user(user.id, user.username or "", user.full_name or "", user.language_code or "uz")
    await log_action(user.id, "\U0001f680 /start", f"full_name={user.full_name}")
    builder = InlineKeyboardBuilder()
    builder.button(text="\U0001f4f1 Mini Ilovani ochish", web_app=WebAppInfo(url=WEBAPP_URL))
    await message.answer(START_TEXT.format(name=user.full_name or "Do'st"), reply_markup=builder.as_markup())
    await message.answer("\U0001f4f2 Yoki asosiy menyudan tanlang:", reply_markup=main_menu_keyboard())


@router.message(F.text == "\U0001f3e0 Asosiy menyu")
async def back_to_main(message: Message):
    await cmd_start(message)


@router.message(F.text == "\U0001f680 Sinov darsiga yozilish")
async def menu_register(message: Message):
    await log_action(message.from_user.id, "\U0001f680 Sinov darsiga yozilish")
    await message.answer(REGISTER_PROMPT, reply_markup=cta_register_keyboard())
