import json
from datetime import datetime

from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from bot.config import CHANNEL_ID
from bot.data.branches import BRANCHES, BRANCH_MAP
from bot.data.courses import COURSES, COURSE_MAP
from bot.database import save_application, save_user
from bot.keyboards.inline import (
    register_branches_keyboard,
    register_courses_keyboard,
    register_time_keyboard,
)
from bot.keyboards.reply import main_menu_keyboard, phone_keyboard

router = Router()


class RegistrationFSM(StatesGroup):
    name      = State()
    phone     = State()
    branch    = State()
    course    = State()
    time_pref = State()


import logging
from bot.config import ADMIN_IDS

logger = logging.getLogger(__name__)


# ─── helpers ──────────────────────────────────────────────────────────────────
async def _send_to_channel(bot: Bot, data: dict, tg_id: int, username: str, source: str = "BOT"):
    now  = datetime.now().strftime("%d.%m.%Y %H:%M")
    text = (
        f"🎓 <b>YANGI ARIZA — SINOV DARSI</b> ({source})\n\n"
        f"👤 <b>Ism:</b> {data.get('full_name','')}\n"
        f"📱 <b>Telefon:</b> {data.get('phone','')}\n"
        f"🏢 <b>Filial:</b> {data.get('branch','')}\n"
        f"📚 <b>Kurs:</b> {data.get('course','')}\n"
        f"⏰ <b>Qulay vaqt:</b> {data.get('time_pref','')}\n"
    )
    if data.get("quiz_score") is not None:
        text += f"📊 <b>Test natijasi:</b> {data['quiz_score']}/15 ({data.get('quiz_level','')})\n"
    text += f"\n🕐 <b>Ariza vaqti:</b> {now}\n🆔 <b>Telegram:</b> @{username} | ID: {tg_id}"

    # 1. Telegram kanalga yuborish
    try:
        await bot.send_message(CHANNEL_ID, text)
        logger.info(f"Kanalga ({CHANNEL_ID}) ariza muvaffaqiyatli yuborildi.")
    except Exception as e:
        logger.error(f"Kanalga ({CHANNEL_ID}) yuborishda xatolik: {e}")

    # 2. Admin(lar)ga shaxsiy xabar yuborish
    for admin_id in ADMIN_IDS:
        if admin_id and admin_id != 0:
            try:
                await bot.send_message(admin_id, f"🔔 <b>YANGI ARIZA KELIB TUSHDI!</b>\n\n{text}")
                logger.info(f"Adminga ({admin_id}) ariza yuborildi.")
            except Exception as e:
                logger.error(f"Adminga ({admin_id}) yuborishda xatolik: {e}")


async def _save_db(tg_id: int, username: str, data: dict):
    await save_user(tg_id, username or None, data.get("full_name") or None)
    await save_application(
        tg_id=tg_id,
        full_name=data.get("full_name", ""),
        phone=data.get("phone", ""),
        branch=data.get("branch", ""),
        course=data.get("course", ""),
        time_pref=data.get("time_pref", ""),
        quiz_score=data.get("quiz_score"),
        quiz_level=data.get("quiz_level"),
    )



# ─── entry: bot button (register_start) ───────────────────────────────────────
@router.callback_query(F.data.in_({"register_start", "register"}))
async def register_start(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.clear()
    await call.message.answer("\U0001f4dd Ismingizni kiriting (To'liq ism va familiya):")
    await state.set_state(RegistrationFSM.name)


# ─── entry: from branch page ──────────────────────────────────────────────────
@router.callback_query(F.data.startswith("register_from_branch:"))
async def register_from_branch(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.clear()
    branch_id   = call.data.split(":")[1]
    branch      = BRANCH_MAP.get(branch_id)
    branch_name = branch.name if branch else branch_id
    await state.update_data(branch=branch_name)
    await call.message.answer(
        f"\U0001f3e2 Filial: <b>{branch_name}</b>\n\n"
        "\U0001f4dd Ismingizni kiriting (To'liq ism va familiya):"
    )
    await state.set_state(RegistrationFSM.name)


# ─── Mini App web_app_data handler ────────────────────────────────────────────
@router.message(F.web_app_data)
async def handle_webapp_data(message: Message):
    try:
        data    = json.loads(message.web_app_data.data)
        tg_id   = message.from_user.id
        uname   = message.from_user.username or ""

        if data.get("type") == "registration":
            full_name = data.get("name", "")
            app_data = {
                "full_name": full_name,
                "phone": data.get("phone", ""),
                "branch": data.get("branch", ""),
                "course": data.get("course", ""),
                "time_pref": data.get("time_pref", ""),
                "quiz_score": str(data["quiz_score"]) if data.get("quiz_score") is not None else None,
                "quiz_level": data.get("quiz_level"),
            }
            await _save_db(tg_id, uname, app_data)
            await _send_to_channel(message.bot, app_data, tg_id, uname, source="MINI APP")

            await message.answer(
                "✅ <b>Arizangiz qabul qilindi!</b>\n\n"
                f"👤 Ism: <b>{full_name}</b>\n"
                f"📱 Tel: <b>{data.get('phone','')}</b>\n"
                f"🏢 Filial: <b>{data.get('branch','')}</b>\n\n"
                "Tez orada menejerimiz siz bilan bog'lanadi! 🤝",
                reply_markup=main_menu_keyboard(),
            )

    except Exception as e:
        await message.answer(f"Xatolik yuz berdi: {e}")


# ─── step 1: name ─────────────────────────────────────────────────────────────
@router.message(StateFilter(RegistrationFSM.name), F.text)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text.strip())
    await message.answer(
        f"\U0001f44d Rahmat, <b>{message.text.strip()}</b>!\n\n"
        "\U0001f4f1 Telefon raqamingizni yuboring:",
        reply_markup=phone_keyboard(),
    )
    await state.set_state(RegistrationFSM.phone)


# ─── step 2: phone ────────────────────────────────────────────────────────────
@router.message(StateFilter(RegistrationFSM.phone), F.contact)
async def get_phone_contact(message: Message, state: FSMContext):
    await _process_phone(message, state, message.contact.phone_number)


@router.message(StateFilter(RegistrationFSM.phone), F.text)
async def get_phone_text(message: Message, state: FSMContext):
    await _process_phone(message, state, message.text.strip())


async def _process_phone(message: Message, state: FSMContext, phone: str):
    await state.update_data(phone=phone)
    data = await state.get_data()
    if data.get("branch"):
        await message.answer("\U0001f4da Kursni tanlang:", reply_markup=register_courses_keyboard(COURSES))
        await state.set_state(RegistrationFSM.course)
    else:
        await message.answer("\U0001f3e2 Filialni tanlang:", reply_markup=register_branches_keyboard(BRANCHES))
        await state.set_state(RegistrationFSM.branch)


# ─── step 3: branch ───────────────────────────────────────────────────────────
@router.callback_query(StateFilter(RegistrationFSM.branch), F.data.startswith("reg_branch:"))
async def get_branch(call: CallbackQuery, state: FSMContext):
    await call.answer()
    branch    = BRANCH_MAP.get(call.data.split(":")[1])
    branch_name = branch.name if branch else call.data.split(":")[1]
    await state.update_data(branch=branch_name)
    await call.message.answer("\U0001f4da Kursni tanlang:", reply_markup=register_courses_keyboard(COURSES))
    await state.set_state(RegistrationFSM.course)


# ─── step 4: course ───────────────────────────────────────────────────────────
@router.callback_query(StateFilter(RegistrationFSM.course), F.data.startswith("reg_course:"))
async def get_course(call: CallbackQuery, state: FSMContext):
    await call.answer()
    course    = COURSE_MAP.get(call.data.split(":")[1])
    course_name = course.name if course else call.data.split(":")[1]
    await state.update_data(course=course_name)
    await call.message.answer("\u23f0 Sizga qulay vaqtni tanlang:", reply_markup=register_time_keyboard())
    await state.set_state(RegistrationFSM.time_pref)


# ─── step 5: time → finish ────────────────────────────────────────────────────
@router.callback_query(StateFilter(RegistrationFSM.time_pref), F.data.startswith("reg_time:"))
async def get_time(call: CallbackQuery, state: FSMContext):
    await call.answer()
    time_value = call.data.split(":", 1)[1]
    await state.update_data(time_pref=time_value)

    data    = await state.get_data()
    tg_id   = call.from_user.id
    uname   = call.from_user.username or ""

    await call.message.answer(
        "\u2705 <b>Arizangiz qabul qilindi!</b>\n\n"
        f"\U0001f464 Ism: <b>{data.get('full_name','')}</b>\n"
        f"\U0001f4f1 Telefon: <b>{data.get('phone','')}</b>\n"
        f"\U0001f3e2 Filial: <b>{data.get('branch','')}</b>\n"
        f"\U0001f4da Kurs: <b>{data.get('course','')}</b>\n"
        f"\u23f0 Qulay vaqt: <b>{time_value}</b>\n\n"
        "Tez orada menejerimiz siz bilan bog'lanadi! \U0001f91d",
        reply_markup=main_menu_keyboard(),
    )
    await _send_to_channel(call.bot, data, tg_id, uname)
    await _save_db(tg_id, uname, data)
    await state.clear()
