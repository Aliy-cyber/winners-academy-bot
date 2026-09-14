from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from bot.data.courses import COURSES, COURSE_MAP
from bot.keyboards.inline import courses_list_keyboard, course_detail_keyboard
from bot.database import log_action

router = Router(name="courses")


@router.message(F.text == "\U0001f4da Kurslarimiz")
async def show_courses(message: Message):
    await log_action(message.from_user.id, "\U0001f4da Kurslarimiz")
    await message.answer(
        "\U0001f4da <b>Bizning kurslarimiz</b>\n\nO'zingizga mos kursni tanlang:",
        reply_markup=courses_list_keyboard(COURSES),
    )


@router.callback_query(F.data.startswith("course:"))
async def show_course_detail(callback: CallbackQuery):
    course_id = callback.data.split(":")[1]
    course = COURSE_MAP.get(course_id)
    if not course:
        await callback.answer("Kurs topilmadi!")
        return
    await log_action(callback.from_user.id, f"\U0001f4da Kurs: {course.name}")
    benefits_text = "\n".join(f"  \u2705 {b}" for b in course.benefits)
    text = (
        f"{course.icon} <b>{course.name}</b>\n\n"
        f"\U0001f465 <b>Kimlar uchun:</b> {course.target}\n"
        f"\u23f1 <b>Davomiyligi:</b> {course.duration}\n\n"
        f"\U0001f4cb <b>Kurs haqida:</b>\n{course.description}\n\n"
        f"\U0001f3af <b>Nimalarga erishasiz:</b>\n{benefits_text}\n\n"
        "\U0001f680 <i>Birinchi sinov darsi <b>BEPUL!</b></i>"
    )
    await callback.message.edit_text(text, reply_markup=course_detail_keyboard())
    await callback.answer()


@router.callback_query(F.data == "back_courses")
async def back_to_courses(callback: CallbackQuery):
    await callback.message.edit_text(
        "\U0001f4da <b>Bizning kurslarimiz</b>\n\nO'zingizga mos kursni tanlang:",
        reply_markup=courses_list_keyboard(COURSES),
    )
    await callback.answer()
