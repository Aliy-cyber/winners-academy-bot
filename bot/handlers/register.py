from datetime import datetime

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from bot.config import CHANNEL_ID
from bot.data.branches import BRANCHES, BRANCH_MAP
from bot.data.courses import COURSES, COURSE_MAP
from bot.database import save_application, save_user
from bot.keyboards.inline import (
    cta_register_keyboard,
    register_branches_keyboard,
    register_courses_keyboard,
    register_time_keyboard,
)
from bot.keyboards.reply import main_menu_keyboard, phone_keyboard

router = Router()


class RegistrationFSM(StatesGroup):
    name = State()
    phone = State()
    branch = State()
    course = State()
    time_pref = State()


# ---------------------------------------------------------------------------
# Entry points
# ---------------------------------------------------------------------------

@router.callback_query(F.data == "register")
async def register_start(call: CallbackQuery, state: FSMContext):
    """Start registration flow — ask for the user's name."""
    await call.answer()
    await state.clear()
    await call.message.answer(
        "\U0001f4dd Ismingizni kiriting (to'liq ism):",
    )
    await state.set_state(RegistrationFSM.name)


@router.callback_query(F.data.startswith("register_from_branch:"))
async def register_from_branch(call: CallbackQuery, state: FSMContext):
    """Pre-select branch and start registration from name step."""
    await call.answer()
    await state.clear()
    branch_id = call.data.split(":")[1]
    branch_name = BRANCH_MAP.get(branch_id, branch_id)
    await state.update_data(branch=branch_name)
    await call.message.answer(
        f"\U0001f3e2 Filial tanlandi: <b>{branch_name}</b>\n\n"
        "\U0001f4dd Ismingizni kiriting (to'liq ism):",
    )
    await state.set_state(RegistrationFSM.name)


# ---------------------------------------------------------------------------
# Step 1 — Name
# ---------------------------------------------------------------------------

@router.message(StateFilter(RegistrationFSM.name), F.text)
async def get_name(message: Message, state: FSMContext):
    """Receive name, ask for phone number."""
    full_name = message.text.strip()
    await state.update_data(full_name=full_name)
    await message.answer(
        f"\U0001f44d Rahmat, <b>{full_name}</b>!\n\n"
        "\U0001f4f1 Telefon raqamingizni yuboring yoki qo'lda kiriting:",
        reply_markup=phone_keyboard(),
    )
    await state.set_state(RegistrationFSM.phone)


# ---------------------------------------------------------------------------
# Step 2 — Phone
# ---------------------------------------------------------------------------

@router.message(StateFilter(RegistrationFSM.phone), F.contact)
async def get_phone_contact(message: Message, state: FSMContext):
    """Receive phone via contact share."""
    phone = message.contact.phone_number
    await _process_phone(message, state, phone)


@router.message(StateFilter(RegistrationFSM.phone), F.text)
async def get_phone_text(message: Message, state: FSMContext):
    """Receive phone typed manually."""
    phone = message.text.strip()
    await _process_phone(message, state, phone)


async def _process_phone(message: Message, state: FSMContext, phone: str):
    await state.update_data(phone=phone)
    data = await state.get_data()
    # If branch was pre-selected (register_from_branch flow), skip branch step
    if data.get("branch"):
        await message.answer(
            "\U0001f4da Kursni tanlang:",
            reply_markup=register_courses_keyboard(COURSES),
        )
        await state.set_state(RegistrationFSM.course)
    else:
        await message.answer(
            "\U0001f3e2 Filialni tanlang:",
            reply_markup=register_branches_keyboard(BRANCHES),
        )
        await state.set_state(RegistrationFSM.branch)


# ---------------------------------------------------------------------------
# Step 3 — Branch
# ---------------------------------------------------------------------------

@router.callback_query(StateFilter(RegistrationFSM.branch), F.data.startswith("reg_branch:"))
async def get_branch(call: CallbackQuery, state: FSMContext):
    """Receive branch selection."""
    await call.answer()
    branch_id = call.data.split(":")[1]
    branch_name = BRANCH_MAP.get(branch_id, branch_id)
    await state.update_data(branch=branch_name)
    await call.message.answer(
        "\U0001f4da Kursni tanlang:",
        reply_markup=register_courses_keyboard(COURSES),
    )
    await state.set_state(RegistrationFSM.course)


# ---------------------------------------------------------------------------
# Step 4 — Course
# ---------------------------------------------------------------------------

@router.callback_query(StateFilter(RegistrationFSM.course), F.data.startswith("reg_course:"))
async def get_course(call: CallbackQuery, state: FSMContext):
    """Receive course selection."""
    await call.answer()
    course_id = call.data.split(":")[1]
    course_name = COURSE_MAP.get(course_id, course_id)
    await state.update_data(course=course_name)
    await call.message.answer(
        "\u23f0 Sizga qulay vaqtni tanlang:",
        reply_markup=register_time_keyboard(),
    )
    await state.set_state(RegistrationFSM.time_pref)


# ---------------------------------------------------------------------------
# Step 5 — Time preference → finalise registration
# ---------------------------------------------------------------------------

@router.callback_query(StateFilter(RegistrationFSM.time_pref), F.data.startswith("reg_time:"))
async def get_time(call: CallbackQuery, state: FSMContext):
    """Receive time preference and complete registration."""
    await call.answer()
    time_value = call.data.split(":")[1]
    await state.update_data(time_pref=time_value)

    data = await state.get_data()
    full_name = data.get("full_name", "")
    phone = data.get("phone", "")
    branch = data.get("branch", "")
    course = data.get("course", "")
    time_pref = time_value
    quiz_score = data.get("quiz_score")
    quiz_level = data.get("quiz_level")

    tg_id = call.from_user.id
    username = call.from_user.username or ""
    now = datetime.now().strftime("%d.%m.%Y %H:%M")

    # Confirmation to user
    await call.message.answer(
        f"\u2705 <b>Arizangiz qabul qilindi!</b>\n\n"
        f"\U0001f464 Ism: <b>{full_name}</b>\n"
        f"\U0001f4f1 Telefon: <b>{phone}</b>\n"
        f"\U0001f3e2 Filial: <b>{branch}</b>\n"
        f"\U0001f4da Kurs: <b>{course}</b>\n"
        f"\u23f0 Qulay vaqt: <b>{time_pref}</b>\n\n"
        "Tez orada menejerimiz siz bilan bog'lanadi! \U0001f91d",
        reply_markup=main_menu_keyboard(),
    )

    # Channel notification card
    channel_text = (
        f"\U0001f393 YANGI ARIZA \u2014 SINOV DARSI\n\n"
        f"\U0001f464 Ism: {full_name}\n"
        f"\U0001f4f1 Telefon: {phone}\n"
        f"\U0001f3e2 Filial: {branch}\n"
        f"\U0001f4da Kurs: {course}\n"
        f"\u23f0 Qulay vaqt: {time_pref}\n"
    )
    if quiz_score is not None:
        channel_text += (
            f"\U0001f4ca Test natijasi: {quiz_score}/15 ({quiz_level})\n"
        )
    channel_text += (
        f"\n\U0001f550 Ariza vaqti: {now}\n"
        f"\U0001f194 Telegram: @{username} | ID: {tg_id}"
    )

    try:
        await call.bot.send_message(CHANNEL_ID, channel_text)
    except Exception:
        pass  # Channel send failure must not break user flow

    # Persist to DB
    await save_user(tg_id, username or None, full_name or None)
    await save_application(
        tg_id=tg_id,
        full_name=full_name,
        phone=phone,
        branch=branch,
        course=course,
        time_pref=time_pref,
        quiz_score=quiz_score,
        quiz_level=quiz_level,
    )

    await state.clear()
